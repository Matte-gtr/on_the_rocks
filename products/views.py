from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required

from site_management.forms import ReviewForm
from products.forms import ProductForm
from .models import Product, Category


def products(request):
    """ Returns a list of paginated products, either all
    products or based on your search term or category filter """

    products = Product.objects.all()
    category_filter = ''
    current_category = ''
    query = ''
    sort = 'category'

    if request.GET:
        if "search" in request.GET:
            query = request.GET.get('search')
            if not query:
                messages.error(request, "No search term entered")
                return redirect(reverse('products'))
            search_results = Q(name__icontains=query) |\
                Q(description__icontains=query) |\
                Q(detail__icontains=query)
            products = products.filter(search_results)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            category_filter = Category.objects.all()
            current_category = request.GET['category']

        if 'sorting' in request.GET:
            sorting = request.GET.get('sorting')
            sort = sorting
            products = products.order_by(sorting)

    template = 'products/products.html'
    product_count = products.count()

    pagi = Paginator(products, 36)
    page_num = request.GET.get('page', 1)
    try:
        page = pagi.page(page_num)
    except EmptyPage:
        page = pagi.page(1)

    context = {
        'products': page,
        'page_header': "Whiskeys",
        'product_count': product_count,
        'category_filter': category_filter,
        'current_category': current_category,
        'search': query,
        'sort': sort,
    }

    return render(request, template, context)


def product_display(request, product_id):
    """ display the details of a product and any associated
    approved reviews """
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                try:
                    review = form.save(commit=False)
                    review.user = request.user
                    review.product = product
                    review.save()
                    messages.success(request, "Thankyou. Your review has been submitted\
                        for review")
                except Exception as e:
                    messages.error(request, f'Review failed: {e}')
        else:
            messages.warning(request, "You have to be logged \
                in to add reviews")
            return redirect(reverse('home'))

    template = 'products/product_display.html'
    form = ReviewForm()
    context = {
        'product': product,
        'form': form,
    }
    return render(request, template, context)


@login_required
def add_product(request):
    """ a view to add a product to the site """
    if request.method == "POST":
        if request.user.is_staff:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save()
                messages.success(request, 'Product added successfully')
                return redirect(reverse('product_display', args=[product.id]))
            else:
                messages.error(request, "Add product failed, please check \
                    the details in the form and re-submit")
        else:
            messages.error(request, 'You do not have the required permissions \
            for this action')
            return redirect(reverse('products'))

    return redirect(reverse('site_management'))


@login_required
def edit_product(request, product_id):
    """ a view to edit a product """
    if request.user.is_staff:
        product = get_object_or_404(Product, pk=product_id)
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, f'{product.name} updated \
                    successfully')
                return redirect(reverse('product_display', args=[product.id]))
            else:
                messages.error(request, 'Update product failed, please check \
                    the details in the form and re-submit')
        else:
            form = ProductForm(instance=product)
            messages.info(request, f'You are editing {product.name}')
    else:
        messages.error(request, 'You do not have the required permissions \
            for this action')
        return redirect(reverse('products'))
    template = 'products/edit_product.html'
    context = {
        'page_header': 'Edit Product',
        'product': product,
        'form': form,
    }
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ a view to delete a a product """
    product = get_object_or_404(Product, pk=product_id)
    if request.user.is_superuser:
        product.delete()
        messages.success(request, f'{product.name} has been successfully \
            deleted')
    else:
        messages.error(request, 'You do not have the required permissions \
            for this action')
    return redirect(reverse('products'))
