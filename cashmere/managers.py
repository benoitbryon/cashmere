from djqmixin import Manager, QMixin


class BalanceMixin(QMixin):
    def unbalanced(self):
        return self.exclude(total_balance=0)

    def balanced(self):
        return self.filter(total_balance=0)


TransactionManager = Manager.include(BalanceMixin)()
