from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import ProductReview, UserProfile
from products.models import Product
from checkout.models import Order
from .forms import UserProfileForm
from products.forms import ProductForm


@login_required
def site_management(request):
    """ display the site management page """
    if request.user.is_staff:
        form = ProductForm()
        template = 'site_management/site_management.html'
        page_header = 'Site Management'
        all_reviews = ProductReview.objects.all()
        reviews = all_reviews.filter(authorised=False)
        context = {
            'page_header': page_header,
            'reviews': reviews,
            'form': form,
        }
    else:
        messages.error(request, 'You need to be assigned as administrator \
            to approve reviews')
        return redirect(reverse('products'))
    return render(request, template, context)


@login_required
def approve_review(request, review_id):
    """ approve a review so it is displayed on the product page """
    if request.user.is_staff:
        try:
            review = get_object_or_404(ProductReview, pk=review_id)
            product = get_object_or_404(Product, pk=review.product_id)
            rating = product.reviews.aggregate(Avg('stars'))['stars__avg']
            review.authorised = True
            review.save(update_fields=['authorised'])
            product.rating = round(rating, 1)
            product.save(update_fields=['rating'])
            messages.success(request, f'{review.product} review by\
                {review.user} approved')
        except Exception as e:
            messages.error(request, f'Error deleting review: {e}')
    else:
        messages.error(request, 'You need to be assigned as administrator \
            to approve reviews')
        return redirect(reverse('products'))
    return redirect(reverse('site_management'))


@login_required
def delete_review(request, review_id):
    """ delete a review that is awaiting authorisation """
    if request.user.is_staff:
        try:
            review = get_object_or_404(ProductReview, pk=review_id)
            review.delete()
            messages.success(request, f'{review.product} review by {review.user}\
                deleted')
        except Exception as e:
            messages.error(request, f'Error deleting review: {e}')
    else:
        messages.error(request, 'You need to be assigned as administrator \
            to approve reviews')
        return redirect(reverse('products'))
    return redirect(reverse('site_management'))


@login_required
def user_profile(request, user_id):
    """ display a users profile with an order history and
    billing/shipping information """
    user_profile = get_object_or_404(UserProfile, pk=user_id)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        current_user = get_object_or_404(User, id=request.user.id)
        if form.is_valid():
            form.save()
            current_user.first_name = user_profile.first_name
            current_user.last_name = user_profile.last_name
            current_user.save()
            messages.success(request, 'Your details have been updated.')
        else:
            messages.error(request, 'The form is invalid, please check \
                the fields and re-submit')
    else:
        form = UserProfileForm(instance=user_profile)
    user_orders = user_profile.orders.all().order_by('-date')
    template = 'site_management/user_profile.html'

    context = {
        'page_header': 'Profile',
        'form': form,
        'user_orders': user_orders,
    }
    return render(request, template, context)


@login_required
def order_history(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template = 'site_management/order_history.html'
    cratelist = []
    for item in order.lineitems.all():
        if item.crate_id:
            if item.crate_id not in cratelist:
                cratelist.append(item.crate_id)
    context = {
        'order': order,
        'cratelist': cratelist,
        'page_header': 'order history',
    }
    return render(request, template, context)
