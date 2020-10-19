from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage

from .forms import ReviewForm
from .models import Product, Category, ProductReview


def products(request):
    """ Returns a list of paginated products, either all
    products or based on your search term """

    products = Product.objects.all()

    if request.GET:
        if "search" in request.GET:
            query = request.GET.get('search')
            if not query:
                messages(request, "No search term entered")
                return redirect(reverse('products'))
            search_results = Q(name__icontains=query) |\
                Q(description__icontains=query) |\
                Q(detail__icontains=query)
            products = products.filter(search_results)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

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
    }

    return render(request, template, context)


def product_display(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        if request.user:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                # messages(request, "Thankyou. Your review has been submitted
                # for review")
            # else:
                # messages(request, "Review failed, please try again")
        # else:
            # messages (request, "You have to be logged in to add reviews")

    template = 'products/product_display.html'
    form = ReviewForm()
    context = {
        'product': product,
        'form': form,
    }
    return render(request, template, context)


@login_required
def site_management(request):
    template = 'products/site_management.html'
    page_header = 'Site Management'
    all_reviews = ProductReview.objects.all()
    reviews = all_reviews.filter(authorised=False)
    context = {
        'page_header': page_header,
        'reviews': reviews,
    }
    return render(request, template, context)


@login_required
def approve_review(request, review_id):
    review = get_object_or_404(ProductReview, pk=review_id)
    if request.user.is_superuser:
        review.authorised = True
        review.save(update_fields=['authorised'])
        # messages(request, f'{review.product} review by {review.user} approved')
    return redirect(reverse('site_management'))
