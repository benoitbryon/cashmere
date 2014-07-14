# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Transaction.total_balance'
        db.add_column(u'cashmere_transaction', 'total_balance',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=2, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Transaction.total_balance'
        db.delete_column(u'cashmere_transaction', 'total_balance')


    models = {
        u'cashmere.account': {
            'Meta': {'unique_together': "(('parent', 'slug'),)", 'object_name': 'Account'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['cashmere.Account']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'cashmere.transaction': {
            'Meta': {'object_name': 'Transaction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '2', 'db_index': 'True'})
        },
        u'cashmere.transactionitem': {
            'Meta': {'ordering': "['-date']", 'object_name': 'TransactionItem'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'operations'", 'to': u"orm['cashmere.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2', 'db_index': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['cashmere.Transaction']"})
        }
    }

    complete_apps = ['cashmere']