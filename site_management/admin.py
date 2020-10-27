from django.contrib import admin
from .models import ProductReview


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


admin.site.register(ProductReview, ProductReviewAdmin)
