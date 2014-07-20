from django.conf.urls import patterns, url

from cashmere import views


dashboard = views.DashboardView.as_view()
account_list = views.AccountListView.as_view()
account_detail = views.AccountDetailView.as_view()
transaction_detail = views.TransactionDetailView.as_view()
operation_create = views.CreateOperationView.as_view()
operation_import = views.ImportOperationsView.as_view()
operation_update = views.EditOperationView.as_view()
operation_list = views.OperationListView.as_view()
cart = views.CartView.as_view()
cart_empty = views.CartEmptyView.as_view()
transaction_merge = views.TransactionMergeView.as_view()
transaction_status = views.TransactionToggleStatusView.as_view()


urlpatterns = patterns(
    '',
    url(r'^$', dashboard, name='dashboard'),
    url(r'^cart/$', cart, name='cart'),
    url(r'^cart/empty/$', cart_empty, name='cart_empty'),
    url(r'^transaction/merge/$', transaction_merge, name='transaction_merge'),
    url(r'^account/$',
        account_detail,
        name='account_list'),
    url(r'^account/(?P<pk>[0-9]+)/$',
        account_detail,
        name='account_detail'),
    url(r'^operation/$',
        operation_list,
        name='operation_list'),
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
    url(r'^transaction/(?P<transaction>[0-9]+)/status/$',
        transaction_status,
        name='transaction_status'),
)
