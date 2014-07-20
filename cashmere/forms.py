import re

from django import forms
from django.utils.translation import ugettext_lazy as _

import django_genericfilters.forms

from cashmere import models


class OperationSearchForm(django_genericfilters.forms.OrderFormMixin,
                          forms.Form):
    account = forms.ModelChoiceField(
        label=_('account'),
        required=False,
        queryset=models.Account.objects,
    )
    date_floor = forms.DateField(
        label=_('from date'),
        required=False,
        input_formats=[
            '%Y-%m-%d',
            '%d/%m/%Y',
        ],
    )
    date_ceil = forms.DateField(
        label=_('to date'),
        required=False,
        input_formats=[
            '%Y-%m-%d',
            '%d/%m/%Y',
        ],
    )
    amount_floor = forms.DecimalField(
        label=_('minimal amount'),
        required=False,
        max_digits=11,
        decimal_places=2,
    )
    amount_ceil = forms.DecimalField(
        label=_('maximal amount'),
        required=False,
        max_digits=11,
        decimal_places=2,
    )

    def get_order_by_choices(self):
        return [
            ('date', _('date')),
            ('amount', _('amount')),
        ]


class CartForm(forms.Form):
    items = forms.ModelMultipleChoiceField(
        label=_('items'),
        queryset=models.Transaction.objects,
    )


class CreateTransactionForm(forms.ModelForm):
    date = forms.DateField(
        label=_('date'),
        required=True,
    )
    amount = forms.DecimalField(
        label=_('amount'),
        max_digits=11,
        decimal_places=2,
        min_value=0,
        required=True,
    )
    origin_account = forms.ModelChoiceField(
        label=_('from'),
        queryset=models.Account.objects,
    )
    destination_account = forms.ModelChoiceField(
        label=_('to'),
        queryset=models.Account.objects,
    )
    description = forms.CharField(
        label=_('description'),
        max_length=200,
    )

    class Meta:
        model = models.Transaction
        fields = [
            'date',
            'amount',
            'origin_account',
            'destination_account',
            'description',
        ]

    def save(self, commit=True):
        instance = super(CreateTransactionForm, self).save(commit=commit)
        origin_operation = models.Operation(
            transaction=instance,
            account=self.cleaned_data['origin_account'],
            amount=-self.cleaned_data['amount'],
            date=self.cleaned_data['date'],
            description=self.cleaned_data['description'],
        )
        destination_operation = models.Operation(
            transaction=instance,
            account=self.cleaned_data['destination_account'],
            amount=self.cleaned_data['amount'],
            date=self.cleaned_data['date'],
            description=self.cleaned_data['description'],
        )
        if commit:
            origin_operation.save()
            destination_operation.save()
        return instance


class CreateOperationForm(forms.ModelForm):
    date = forms.DateField(
        label=_('date'),
        required=True,
        input_formats=[
            '%Y-%m-%d',
            '%d/%m/%Y',
        ],
    )
    amount = forms.DecimalField(
        label=_('amount'),
        max_digits=11,
        decimal_places=2,
        required=True,
        localize=True,
    )
    account = forms.ModelChoiceField(
        label=_('account'),
        queryset=models.Account.objects,
    )
    description = forms.CharField(
        label=_('description'),
        max_length=200,
    )
    transaction = forms.ModelChoiceField(
        label=_('transaction'),
        queryset=models.Transaction.objects,
        widget=forms.HiddenInput,
    )
    splits = forms.IntegerField(
        label=_('splits'),
        initial=1,
        min_value=1,
        required=False,
    )

    class Meta:
        model = models.Operation

    def clean_description(self):
        value = self.cleaned_data['description']
        value = re.sub(r'\s+', ' ', value)
        return value


class EditOperationForm(forms.ModelForm):
    class Meta:
        model = models.Operation
        fields = ['date', 'amount', 'description']


class ImportOperationsForm(forms.Form):
    account = forms.ModelChoiceField(
        label=_('account'),
        queryset=models.Account.objects,
    )
    operations = forms.FileField(
        label=_('operations'),
    )
