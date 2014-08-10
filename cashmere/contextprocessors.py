from cashmere import models


def accounts(request):
    return {
        'accounts': models.Account.objects.all(),
    }
