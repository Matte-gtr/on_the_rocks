from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage

from .forms import ReviewForm
from .models import Product, Category, ProductReview


def products(request):
    """ Returns a list of paginated products, either all
    products or based on your search term or category filter """

    products = Product.objects.all()
    category_filter = ''
    current_category = ''
    query = ''

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
            category_filter = Category.objects.all()
            current_category = request.GET['category']

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
                review = form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                # messages(request, "Thankyou. Your review has been submitted
                # for review")
            # else:
                # messages(request, "Review failed, please try again")
        else:
            return redirect(reverse('home'))  # test purposes
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
    """ display the site management page """
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
    """ approve a review so it is displayed on the product page """
    review = get_object_or_404(ProductReview, pk=review_id)

    product = get_object_or_404(Product, pk=review.product_id)
    rating = product.reviews.aggregate(Avg('stars'))['stars__avg']

    if request.user.is_superuser:
        review.authorised = True
        review.save(update_fields=['authorised'])
        product.rating = round(rating, 1)
        product.save(update_fields=['rating'])
        messages.info(request, f'{review.product} review by\
            {review.user} approved')
    else:
        messages.error(request, 'You need to be assigned as administrator \
            to do that')

    return redirect(reverse('site_management'))


@login_required
def delete_review(request, review_id):
    """ delete a review that is awaiting authorisation """
    review = get_object_or_404(ProductReview, pk=review_id)
    if request.user.is_superuser:
        review.delete()
        messages.warning(request, f'{review.product} review by {review.user}\
            deleted')
    return redirect(reverse('site_management'))
