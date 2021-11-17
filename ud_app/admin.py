from django.contrib import admin
from .models import Account, Category, Product
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

class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('category_name',)}

    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('product_name',)}

    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')

admin.site.register(Product,ProductAdmin)