from django.contrib import admin
from .models import Category, Product, ProductReview


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'friendly_name',
    ]


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'detail',
        'size',
        'proof',
        'price',
    ]
    ordering = [
        'name',
    ]


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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
