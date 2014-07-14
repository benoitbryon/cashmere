from django.conf.urls import patterns, url

from cashmere import views


dashboard = views.DashboardView.as_view()
account_list = views.AccountListView.as_view()
account_detail = views.AccountDetailView.as_view()
transaction_detail = views.TransactionDetailView.as_view()
operation_create = views.CreateOperationView.as_view()
operation_import = views.ImportOperationsView.as_view()
operation_update = views.EditOperationView.as_view()


urlpatterns = patterns(
    '',
    url(r'^$', dashboard, name='dashboard'),
    url(r'^account/$', account_list, name='account_list'),
    url(r'^account/(?P<pk>[0-9]+)/$',
        account_detail,
        name='account_detail'),
    url(r'^operation/import/$',
        operation_import,
        name='operation_import'),
    url(r'^operation/(?P<pk>[0-9]+)/$',
        operation_update,
        name='operation_edit'),
    url(r'^transaction/(?P<pk>[0-9]+)/$',
        transaction_detail,
        name='transaction_detail'),
    url(r'^transaction/(?P<transaction>[0-9]+)/add/$',
        operation_create,
        name='operation_create'),
)
