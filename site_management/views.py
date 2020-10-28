from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import ProductReview
from products.models import Product


@login_required
def site_management(request):
    """ display the site management page """
    template = 'site_management/site_management.html'
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
        messages.success(request, f'{review.product} review by\
            {review.user} approved')
    else:
        messages.error(request, 'You need to be assigned as administrator \
            to approve reviews')

    return redirect(reverse('site_management'))


@login_required
def delete_review(request, review_id):
    """ delete a review that is awaiting authorisation """
    if request.user.is_superuser:
        try:
            review = get_object_or_404(ProductReview, pk=review_id)
            review.delete()
            messages.success(request, f'{review.product} review by {review.user}\
                deleted')
        except Exception as e:
            messages.error(request, f'Error deleting review: {e}')
    return redirect(reverse('site_management'))


@login_required
def user_profile(request, user_id):
    """ display a users profile with an order history and
    billing/shipping information """
    template = 'site_management/user_profile.html'
    context = {
        'page_header': 'Profile'
    }
    return render(request, template, context)