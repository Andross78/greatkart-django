
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from ud_app.views import (
    home,
    store,
    product_detail,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('store/', store, name='store'),
    path('store/<slug:category_slug>/', store, name='products_by_category'),
    path('store/<slug:category_slug>/<slug:product_slug>/', product_detail, name='products_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
