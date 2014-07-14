import calendar
import datetime
import decimal

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from dateutil.relativedelta import relativedelta
from mptt.models import MPTTModel, TreeForeignKey

from cashmere import managers


class Account(MPTTModel):
    """A bank account emits or receives operations."""
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children')
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['slug']

    class Meta:
        unique_together = (('parent', 'slug'))

    def __unicode__(self):
        if self.is_root_node():
            return self.slug
        else:
            return u'{parent:s} / {slug:s}'.format(
                parent=self.parent,
                slug=self.slug)

    def get_absolute_url(self):
        return reverse('ui:account_detail', args=[self.pk])

    def balance(self, date=None):
        if date is None:
            date = now()
        data = Operation.objects \
                        .filter(account__lft__gte=self.lft,
                                account__rght__lte=self.rght,
                                account__tree_id=self.tree_id) \
                        .filter(date__lte=date) \
                        .aggregate(balance=models.Sum('amount')) \
                        .values()[0]
        return data

    def month_balance(self, date=None):
        """Return estimated balance for end of month."""
        if date is None:
            date = now().date()
        last_day_in_month = datetime.date(
            date.year,
            date.month,
            calendar.monthrange(date.year, date.month)[1]
        )
        return self.balance(last_day_in_month)

    def last_month_balance(self):
        """Return balance for end of last month."""
        today = now().date()
        one_month_before = today - relativedelta(months=1)
        return self.month_balance(one_month_before)

    def next_month_balance(self):
        """Return estimated balance for end of next month."""
        today = now().date()
        one_month_after = today + relativedelta(months=1)
        return self.month_balance(one_month_after)


class Transaction(models.Model):
    """Operation record between accounts.

    One transaction is made of several :class:`Operation`.

    Balance of a transaction must be 0, or it is not complete.

    """
    #: The balance of all operations in the transaction, whatever their date.
    total_balance = models.DecimalField(
        _('balance'),
        max_digits=11,
        decimal_places=2,
        db_index=True,
        default=decimal.Decimal(0),
        editable=False)

    objects = managers.TransactionManager

    def get_absolute_url(self):
        return reverse('ui:transaction_detail', args=[self.pk])

    def balance(self, date=None):
        operations = self.operations.all()
        if date:
            operations = operations.filter(date__lte=date)
        balance = operations.aggregate(balance=models.Sum('amount')) \
                            .values()[0]
        if balance is None:  # No transaction.
            balance = decimal.Decimal(0)
        return balance


class Operation(models.Model):
    """Operation record in a transaction, for one account."""
    transaction = models.ForeignKey(Transaction, related_name='operations')
    account = models.ForeignKey(Account, related_name='operations')
    date = models.DateField(_('date'), db_index=True)
    amount = models.DecimalField(
        _('amount'),
        max_digits=11,
        decimal_places=2,
        db_index=True)
    description = models.CharField(_('description'), max_length=200)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return '{amount} as "{description}" on {date}'.format(
            amount=self.amount,
            description=self.description,
            date=self.date)

    def is_debit(self):
        return self.amount < 0

    def is_credit(self):
        return self.amount >= 0


def update_transaction_balance(sender, **kwargs):
    operation = kwargs['instance']
    operation.transaction.total_balance = operation.transaction.balance()
    operation.transaction.save()


signals.post_save.connect(update_transaction_balance, sender=Operation)
signals.post_delete.connect(update_transaction_balance, sender=Operation)
