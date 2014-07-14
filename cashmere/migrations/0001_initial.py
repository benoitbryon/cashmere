# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'cashmere_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['cashmere.Account'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'cashmere', ['Account'])

        # Adding unique constraint on 'Account', fields ['parent', 'slug']
        db.create_unique(u'cashmere_account', ['parent_id', 'slug'])

        # Adding model 'Transaction'
        db.create_table(u'cashmere_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'cashmere', ['Transaction'])

        # Adding model 'TransactionItem'
        db.create_table(u'cashmere_transactionitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['cashmere.Transaction'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='operations', to=orm['cashmere.Account'])),
            ('date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cashmere', ['TransactionItem'])


    def backwards(self, orm):
        # Removing unique constraint on 'Account', fields ['parent', 'slug']
        db.delete_unique(u'cashmere_account', ['parent_id', 'slug'])

        # Deleting model 'Account'
        db.delete_table(u'cashmere_account')

        # Deleting model 'Transaction'
        db.delete_table(u'cashmere_transaction')

        # Deleting model 'TransactionItem'
        db.delete_table(u'cashmere_transactionitem')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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