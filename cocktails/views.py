from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage

from .models import Cocktail


def cocktails(request):
    """ a view to display a list of all cocktails """
    cocktails = Cocktail.objects.all()

    pagi = Paginator(cocktails, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = pagi.page(page_num)
    except EmptyPage:
        page = pagi.page(1)

    template = 'cocktails/cocktails.html'
    context = {
        'page_header': 'Cocktails',
        'cocktails': cocktails,
    }
    return render(request, template, context)


def display_cocktail(request, cocktail_id):
    """ a view to display an idividual cocktail recipe """
    cocktail = get_object_or_404(Cocktail, pk=cocktail_id)

    template = 'cocktails/display_cocktail.html'
    context = {
        'page_header': 'cocktail recipe',
        'cocktail': cocktail,
    }
    return render(request, template, context)
