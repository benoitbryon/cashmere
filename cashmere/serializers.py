from rest_framework import serializers

from cashmere import models


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Account
        fields = ('parent', 'slug')


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Transaction


class OperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Operation
        fields = ('transaction', 'account', 'date', 'amount', 'description')
