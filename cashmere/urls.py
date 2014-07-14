from django.conf.urls import include, patterns, url

from rest_framework import routers

from cashmere import views


router = routers.DefaultRouter()
router.register(r'account', views.AccountViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'operations', views.OperationViewSet)


transaction_create = views.CreateTransactionView.as_view()


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'^api/transaction/create/$',
        transaction_create,
        name='transaction_create'),
    url(r'^api/', include(router.urls)),
    url(r'^ui/', include('cashmere.ui_urls', namespace='ui', app_name='ui')),
)
