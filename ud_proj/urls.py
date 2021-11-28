
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from ud_app.views import (
    home,
    store,
    product_detail,
    cart,
    add_cart,
    remove_cart,
    remove_cart_item,
    search,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('store/', store, name='store'),
    path('store/category/<slug:category_slug>/', store, name='products_by_category'),
    path('store/category/<slug:category_slug>/<slug:product_slug>/', product_detail, name='products_detail'),
    path('cart/', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', remove_cart_item, name='remove_cart_item'),
    path('store/search/', search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
