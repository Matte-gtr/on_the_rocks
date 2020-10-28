from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ['lineitem_total']

    fields = ['order', 'product', 'crate_id', 'quantity', 'lineitem_total']


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ['order_number', 'user_profile', 'date',
                       'shipping_cost', 'order_cost',
                       'grand_total', 'cart_contents',
                       'stripe_pid']

    fields = ['order_number', 'user_profile', 'date', 'first_name',
              'last_name', 'email', 'contact_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'shipping_cost',
              'order_cost', 'grand_total', 'cart_contents', 'stripe_pid']

    list_display = ['order_number', 'user_profile', 'date', 'first_name',
                    'last_name', 'order_cost', 'shipping_cost',
                    'grand_total']

    ordering = ['-date']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLineItem)
