from django.contrib import admin
from .models import ProductReview, UserProfile


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'created_on',
        'product',
        'stars',
        'review',
        'anon',
        'authorised',
    ]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'first_name',
        'last_name',
        'email',
        'contact_number',
        'street_address1',
        'street_address2',
        'town_or_city',
        'postcode',
        'county',
        'country'
    ]


admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
