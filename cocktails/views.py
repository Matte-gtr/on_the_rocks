from django.shortcuts import render
from .models import Cocktail


def cocktails(request):
    """ a view to display a list of all cocktails """
    cocktails = Cocktail.objects.all()
    template = 'cocktails/cocktails.html'
    context = {
        'page_header': 'Cocktails',
        'cocktails': cocktails,
    }
    return render(request, template, context)
