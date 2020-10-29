from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cocktail
from .forms import CocktailForm


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
        'cocktails': page,
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


@login_required
def delete_cocktail(request, cocktail_id):
    """ a view to delete a a cocktail """
    cocktail = get_object_or_404(Cocktail, pk=cocktail_id)
    if request.user.is_superuser:
        cocktail.delete()
        messages.success(request, f'{cocktail.name} has been successfully \
            deleted')
    else:
        messages.error(request, 'You do not have the required permissions \
            for this action')
    return redirect(reverse('cocktails'))


@login_required
def add_cocktail(request):
    """ a view to add a cocktail to the database/site """
    if request.method == "POST":
        if request.user.is_staff:
            form = CocktailForm(request.POST, request.FILES)
            if form.is_valid():
                cocktail = form.save()
                messages.success(request, 'Cocktail added successfully')
                return redirect(reverse('display_cocktail',
                                args=[cocktail.id]))
            else:
                messages.error(request, "Add cocktail failed, please check \
                    the details in the form and re-submit")
        else:
            messages.error(request, 'You do not have the required permissions \
            for this action')
            return redirect(reverse('products'))

    return redirect(reverse('site_management'))


@login_required
def edit_cocktail(request, cocktail_id):
    """ a view to edit a cocktail recipe """
    if request.user.is_staff:
        cocktail = get_object_or_404(Cocktail, pk=cocktail_id)
        if request.method == "POST":
            form = CocktailForm(request.POST, request.FILES, instance=cocktail)
            if form.is_valid():
                form.save()
                messages.success(request, f'{cocktail.name} updated \
                    successfully')
                return redirect(reverse('display_cocktail',
                                args=[cocktail.id]))
            else:
                messages.error(request, 'Update product failed, please check \
                    the details in the form and re-submit')
        else:
            form = CocktailForm(instance=cocktail)
            messages.info(request, f'You are editing {cocktail.name}')
    else:
        messages.error(request, 'You do not have the required permissions \
            for this action')
        return redirect(reverse('cocktails'))
    template = 'cocktails/edit_cocktail.html'
    context = {
        'page_header': 'Edit Cocktail',
        'cocktail': cocktail,
        'form': form,
    }
    return render(request, template, context)
