import csv
import datetime
import decimal

from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum
from django.utils.timezone import now
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from django.views.generic import FormView, UpdateView, RedirectView

from dateutil.relativedelta import relativedelta
from django_genericfilters.views import FilteredListView
from rest_framework import viewsets

from cashmere import forms
from cashmere import models
from cashmere import serializers


class OperationListView(FilteredListView):
    """List of operations, whatever the transaction."""
    model = models.Operation
    form_class = forms.OperationSearchForm

    def form_valid(self, form):
        queryset = super(OperationListView, self).form_valid(form)
        if form.cleaned_data['account']:
            account = form.cleaned_data['account']
            queryset = queryset.filter(
                account__lft__gte=account.lft,
                account__rght__lte=account.rght,
                account__tree_id=account.tree_id)
        if form.cleaned_data['date_floor']:
            queryset = queryset.filter(
                date__gte=form.cleaned_data['date_floor'])
        if form.cleaned_data['date_ceil']:
            queryset = queryset.filter(
                date__lte=form.cleaned_data['date_ceil'])
        if form.cleaned_data['amount_floor']:
            queryset = queryset.filter(
                amount__gte=form.cleaned_data['amount_floor'])
        if form.cleaned_data['amount_ceil']:
            queryset = queryset.filter(
                amount__lte=form.cleaned_data['amount_ceil'])
        return queryset

    def get_context_data(self, **kwargs):
        data = super(OperationListView, self).get_context_data(**kwargs)
        data['balance'] = data['object_list'] \
            .aggregate(balance=Sum('amount')) \
            .values()[0]
        return data


class CartView(FormView):
    form_class = forms.CartForm
    success_url = reverse_lazy('ui:dashboard')
    template_name = 'cashmere/cart.html'

    def form_valid(self, form):
        if 'cart' not in self.request.session:
            self.request.session['cart'] = []
        cart = self.request.session['cart']
        for transaction in form.cleaned_data['items']:
            if transaction.pk not in cart:
                cart.append(transaction.pk)
        self.request.session['cart'] = cart
        return super(CartView, self).form_valid(form)


class TransactionMergeView(RedirectView):
    """Merge transactions into one."""
    def get_redirect_url(self, **kwargs):
        if self.request.session['cart']:
            new_transaction = models.Transaction.objects.create()
            transactions = models.Transaction.objects.filter(
                id__in=self.request.session['cart'])
            for transaction in transactions:
                for operation in transaction.operations.all():
                    operation.transaction = new_transaction
                    operation.save()
                transaction.delete()
            self.request.session['cart'] = []
            return reverse('ui:transaction_detail', args=[new_transaction.pk])
        else:
            return reverse('ui:dashboard')


class TransactionToggleStatusView(RedirectView):
    """Toggle transaction status (open or close)."""
    def get_redirect_url(self, **kwargs):
        transaction_id = self.kwargs['transaction']
        transaction = models.Transaction.objects.get(pk=transaction_id)
        transaction.is_open = not transaction.is_open
        transaction.save()
        return reverse('ui:transaction_detail', args=[transaction.pk])


class CartEmptyView(RedirectView):
    def get_redirect_url(self):
        self.request.session['cart'] = []
        return reverse('ui:dashboard')


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer


class OperationViewSet(viewsets.ModelViewSet):
    queryset = models.Operation.objects.all()
    serializer_class = serializers.OperationSerializer


class AccountListView(ListView):
    model = models.Account

    def get_context_data(self, **kwargs):
        data = ListView.get_context_data(self, **kwargs)
        populate_monthly_amounts(data['object_list'])
        return data


class AccountDetailView(DetailView):
    model = models.Account

    def get_context_data(self, **kwargs):
        data = DetailView.get_context_data(self, **kwargs)
        data['operations'] = \
            models.Operation.objects \
                            .filter(account__lft__gte=self.object.lft,
                                    account__rght__lte=self.object.rght,
                                    account__tree_id=self.object.tree_id) \
                            .select_related('transaction')
        max_amount = 0
        for operation in data['operations']:
            operation.relative_width = abs(int(operation.amount / 10))
            if operation.relative_width > max_amount:
                max_amount = operation.relative_width
        for operation in data['operations']:
            try:
                operation.relative_width = int(
                    operation.relative_width * 100 / max_amount)
            except ZeroDivisionError:
                operation.relative_width = 0
            if operation.relative_width == 0 and abs(operation.amount) >= 1:
                operation.relative_width = 1
        data['import_operations_form'] = forms.ImportOperationsForm(
            initial={'account': self.object.pk})
        populate_monthly_amount(data['object'])
        data['descendants'] = data['object'].get_descendants()
        populate_monthly_amounts(data['descendants'])
        month_list = []
        today = now().date()
        account = data['object']
        max_balance = None
        for month_delta in range(-12, 1):
            date_floor = today + relativedelta(months=month_delta)
            date_floor = datetime.date(date_floor.year, date_floor.month, 1)
            date_ceil = date_floor + relativedelta(months=1)
            date_ceil = datetime.date(date_ceil.year, date_ceil.month, 1)
            amount = models.Operation.objects \
                .filter(account__lft__gte=account.lft,
                        account__rght__lte=account.rght,
                        account__tree_id=account.tree_id) \
                .filter(
                    date__gte=date_floor,
                    date__lt=date_ceil) \
                .aggregate(balance=Sum('amount')) \
                .values()[0]
            if amount is None:
                average = decimal.Decimal('0.00')
            else:
                average = amount
                average = average.quantize(decimal.Decimal('0.01'))
            month_list.append({
                'year': date_floor.year,
                'title': date_floor.strftime('%B %Y'),
                'balance': average,
                'relative_balance': 0,
            })
            if abs(average) > max_balance:
                max_balance = abs(average)
        for month in month_list:
            month['relative_balance'] = int(
                abs(month['balance']) * 100 / max_balance)
        data['month_list'] = month_list
        return data


class TransactionDetailView(DetailView):
    model = models.Transaction
    template_name = 'cashmere/transaction_detail.html'

    def get_context_data(self, **kwargs):
        data = DetailView.get_context_data(self, **kwargs)
        data['operations'] = self.object.operations.all()
        for operation in data['operations']:
            operation.edit_form = forms.EditOperationForm(instance=operation)
        data['create_operation_form'] = forms.CreateOperationForm(
            initial={'transaction': self.object.pk})
        return data


def delete_empty_transactions():
    """Clean database by deleting transactions with no operations."""
    models.Transaction.objects \
                      .filter(operations__pk__isnull=True) \
                      .filter(total_balance=0) \
                      .delete()


def populate_monthly_amount(account):
    """Assign ``monthly_amount`` attribute to ``account``."""
    account.monthly_amount = {}
    for delta in [1, 3, 6, 12]:
        date_floor = now() - relativedelta(months=delta)
        date_floor = datetime.date(
            year=date_floor.year,
            month=date_floor.month,
            day=1)
        date_ceil = now() + relativedelta(months=1)
        date_ceil = datetime.date(
            year=date_ceil.year,
            month=date_ceil.month,
            day=1)
        amount = models.Operation.objects \
            .filter(account__lft__gte=account.lft,
                    account__rght__lte=account.rght,
                    account__tree_id=account.tree_id) \
            .filter(
                date__gte=date_floor,
                date__lt=date_ceil) \
            .aggregate(balance=Sum('amount')) \
            .values()[0]
        if amount is None:
            average = decimal.Decimal('0.00')
        else:
            average = amount / delta
            average = average.quantize(decimal.Decimal('0.01'))
        account.monthly_amount[delta] = average


def populate_monthly_amounts(accounts):
    """Assign ``monthly_amount`` attribute to ``accounts`` queryset."""
    for account in accounts:
        populate_monthly_amount(account)


class DashboardView(TemplateView):
    template_name = 'cashmere/dashboard.html'

    def get_context_data(self, **kwargs):
        delete_empty_transactions()  # Maintenance.
        data = TemplateView.get_context_data(self, **kwargs)
        data['create_transaction_form'] = forms.CreateTransactionForm(
            initial={'date': now()})
        data['account_list'] = models.Account.objects.all()
        populate_monthly_amounts(data['account_list'])
        # Recent operations: N latest operations from now.
        data['recent_operations'] = models.Operation.objects \
            .filter(date__lte=now().date()) \
            .order_by('-date')[0:5]
        # Next operations: N next operations from now.
        data['next_operations'] = models.Operation.objects \
            .filter(date__gt=now().date()) \
            .order_by('date')[0:5]
        # Unbalanced transactions.
        data['unbalanced_transactions'] = \
            models.Transaction.objects.unbalanced()[0:10]
        self.request.session.setdefault('cart', [])
        data['cart'] = {
            'items': models.Transaction.objects.filter(
                id__in=self.request.session['cart']),
        }
        return data


class CreateTransactionView(CreateView):
    model = models.Transaction
    form_class = forms.CreateTransactionForm


def split_amount(amount, splits, places=2):
    """Return list of ``splits`` amounts where sum of items equals ``amount``.

    >>> from decimal import Decimal
    >>> split_amount(Decimal('12'), 1)
    Decimal('12.00')
    >>> split_amount(Decimal('12'), 2)
    [Decimal('6.00'), Decimal('6.00')]

    Amounts have a max of ``places`` decimal places. Last amount in the list
    may not be the same as others (will always be lower than or equal to
    others).

    >>> split_amount(Decimal('100'), 3)
    [Decimal('33,34'), Decimal('33,34'), Decimal('33,32')]
    >>> split_amount(Decimal('100'), 3, 4)
    [Decimal('33,3334'), Decimal('33,3334'), Decimal('33,3332')]
    >>> split_amount(Decimal('12'), 7)  # Doctest: +ELLIPSIS
    [Decimal('1.72'), ..., Decimal('1.72'), ..., Decimal('1.68')]
    >>> split_amount(Decimal('12'), 17)  # Doctest: +ELLIPSIS
    [Decimal('0.71'), ..., Decimal('0.71'), Decimal('0.64')]

    """
    one = decimal.Decimal(10) ** -places
    amount = amount.quantize(one)
    with decimal.localcontext() as decimal_context:
        decimal_context.rounding = decimal.ROUND_UP
        upper_split = (amount / splits).quantize(one)
    splitted_amounts = [upper_split] * (splits - 1)
    lower_split = amount - sum(splitted_amounts)
    splitted_amounts.append(lower_split)
    return splitted_amounts


class CreateOperationView(FormView):
    model = models.Operation
    form_class = forms.CreateOperationForm

    def form_valid(self, form):
        """Create operation with optional splits."""
        self.form = form
        date = form.cleaned_data['date']
        if form.cleaned_data['splits'] == 1:
            models.Operation.objects.create(
                account=form.cleaned_data['account'],
                transaction=form.cleaned_data['transaction'],
                date=date,
                amount=form.cleaned_data['amount'],
                description=form.cleaned_data['description'],
            )
        else:
            splits = split_amount(
                form.cleaned_data['amount'],
                form.cleaned_data['splits'])
            for position, amount in enumerate(splits):
                description = u'{desc} ({total}/{splits}, part {pos})'.format(
                    desc=form.cleaned_data['description'],
                    pos=position + 1,
                    splits=form.cleaned_data['splits'],
                    total=form.cleaned_data['amount'])
                models.Operation.objects.create(
                    account=form.cleaned_data['account'],
                    transaction=form.cleaned_data['transaction'],
                    date=date + relativedelta(months=position),
                    amount=amount,
                    description=description,
                )
        return FormView.form_valid(self, form)

    def get_success_url(self):
        return reverse('ui:transaction_detail',
                       args=[self.form.cleaned_data['transaction'].pk])


class EditOperationView(UpdateView):
    model = models.Operation
    form_class = forms.EditOperationForm

    def form_valid(self, form):
        self.form = form
        return super(EditOperationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('ui:transaction_detail',
                       args=[self.form.instance.transaction.pk])


class ImportOperationsView(FormView):
    form_class = forms.ImportOperationsForm
    template_name = 'cashmere/operation_import.html'

    def form_valid(self, form):
        account = form.cleaned_data['account']
        csv_reader = csv.reader(form.cleaned_data['operations'])
        with_headers = True
        columns = ['date', 'description', 'amount']
        if with_headers:
            csv_reader.next()
        for line in csv_reader:
            data = dict([
                (field, line[position])
                for position, field in enumerate(columns)
                if field is not None
            ])
            data['account'] = account.pk
            data['transaction'] = models.Transaction.objects.create().pk
            operation_form = forms.CreateOperationForm(data=data)
            if operation_form.is_valid():
                operation_form.save()
        self.form = form
        return super(ImportOperationsView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'ui:account_detail',
            args=[self.form.cleaned_data['account'].pk])
