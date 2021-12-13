
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from ud_app.views import (
    register,
    login,
    logout,
    activate,
    home,
    store,
    product_detail,
    cart,
    add_cart,
    remove_cart,
    remove_cart_item,
    checkout,
    search,
    dashboard,
    my_orders,
    edit_profile,
    change_password,
    order_detail,
    forgot_password,
    resetpassword_validate,
    reset_password,
    place_order,
    payments,
    order_complete,
    submit_review,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('store/', store, name='store'),
    path('store/category/<slug:category_slug>/', store, name='products_by_category'),
    path('store/category/<slug:category_slug>/<slug:product_slug>/', product_detail, name='products_detail'),
    # cart
    path('cart/', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', remove_cart_item, name='remove_cart_item'),
    path('checkout/', checkout, name='checkout'),

    path('store/search/', search, name='search'),
    # account
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('dashboard/', dashboard, name='dashboard'),
    path('my_orders/', my_orders, name='my_orders'),
    path('edit_profile/',edit_profile, name='edit_profile'),
    path('change_password/',change_password, name='change_password'),
    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),

    path('forgotPassword/', forgot_password, name='forgot_password'),
    path('resetpassword_validate/<uidb64>/<token>', resetpassword_validate, name='resetpassword_validate'),
    path('reset_password/', reset_password, name='reset_password'),

    # orders
    path('place_order/', place_order, name='place_order'),
    path('payments/', payments, name='payments'),
    path('order_complete/', order_complete, name='order_complete'),
    path('submit_review/<int:product_id>/', submit_review, name='submit_review')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
