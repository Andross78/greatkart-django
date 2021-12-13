from django.contrib import admin
from django.utils.html import format_html

from .models import Account, UserProfile, Category, Product, Cart, CartItem, Variation, Payment, OrderProduct, Order, RevievRating
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):

    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')

    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)


class UserProfileAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border_radius:50%;">'.format(object.profile_pictures.url))

    thumbnail.short_description = "Profile Picture"

    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

admin.site.register(UserProfile, UserProfileAdmin)


class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('category_name',)}

    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('product_name',)}

    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')

admin.site.register(Product,ProductAdmin)


class CartAdmin(admin.ModelAdmin):

    list_display = ('card_id', 'date_added')


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):

    list_display = ('product', 'cart', 'quantity', 'is_active')


admin.site.register(CartItem, CartItemAdmin)


class VariationAdmin(admin.ModelAdmin):

    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')

admin.site.register(Variation, VariationAdmin)


class OrderProductInline(admin.TabularInline):

    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'order')
    extra = 0


class OrderAdmin(admin.ModelAdmin):

    list_display = ['order_number', 'first_name', 'last_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status',
                    'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20

    inlines = [OrderProductInline]


admin.site.register(Order, OrderAdmin)


class OrderProductAdmin(admin.ModelAdmin):

    list_display = ['payment', 'quantity', 'product_price', 'created_at', 'updated_at']
    list_filter = ['ordered', 'payment', 'created_at']
    search_fields = ['payment']

admin.site.register(OrderProduct, OrderProductAdmin)

admin.site.register(Payment)

admin.site.register(RevievRating)