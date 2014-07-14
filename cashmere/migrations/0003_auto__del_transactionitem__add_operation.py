# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.contrib.contenttypes.models import ContentType


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table(u'cashmere_transactionitem', u'cashmere_operation')
        if not db.dry_run:
            ContentType \
                .objects \
                .filter(app_label='cashmere', model='transactionitem') \
                .update(model='operation')

    def backwards(self, orm):
        db.rename_table(u'cashmere_operation', u'cashmere_transactionitem')
        if not db.dry_run:
            ContentType \
                .objects \
                .filter(app_label='cashmere', model='operation') \
                .update(model='transactionitem')

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
        u'cashmere.operation': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Operation'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'operations'", 'to': u"orm['cashmere.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2', 'db_index': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'operations'", 'to': u"orm['cashmere.Transaction']"})
        },
        u'cashmere.transaction': {
            'Meta': {'object_name': 'Transaction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '11', 'decimal_places': '2', 'db_index': 'True'})
        }
    }

    complete_apps = ['cashmere']
