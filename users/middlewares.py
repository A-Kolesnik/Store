from products.models import Buscet


def buscets_processor(request):
    """Формирует поле контекста 'buscets', описывающего корзину пользователя"""
    context = {
        'buscets': Buscet.objects.select_related(
            'user',
            'product'
        ).filter(
            user__id=request.user.id
        ).values(
            'id',
            'total',
            'price',
            'user__id',
            'product__name',
            'product__price',
        )
    } if request.user.id else {}

    Buscet.objects.select_related(None)

    return context
