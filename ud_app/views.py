from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from .models import Account, Product, Category, Cart, CartItem, Variation
from .forms import RegistrationForm


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.')
            return redirect('/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'register.html', context)

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):

    auth.logout(request)
    messages.success(request, "You are logged out")

    return redirect('login')


def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations, your account is activated.')

        return redirect('login')

    else:
        messages.error(request, 'Invalid activation link')

        return redirect('register')


    return HttpResponse('you are activated')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


def forgot_password(request):

    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent!')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')
    return render(request, 'forgotPassword.html')


def resetpassword_validate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):

        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('login')


    return HttpResponse('ok')


def reset_password(request):

    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('reset_password')
    else:
        return render(request, 'reset_password.html')


def home(request):

    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }

    return render(request, 'home.html', context)


def store(request, category_slug=None):

    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)


def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__card_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }
    return render(request, 'product_detail.html', context)


def _cart_id(request):

    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except Exception:
                print('=====')

    try:
        cart = Cart.objects.get(card_id=_cart_id(request)) # get the cart using cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            card_id=_cart_id(request)
        )

    cart.save()

    is_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()


    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product, cart=cart)

        # existing variations -> database
        # current variation -> product_variations
        # item_id -> database

        ex_var_list = []
        id = []

        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        print(ex_var_list)

        if product_variation in ex_var_list:
            # increase cart_item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):

    cart = Cart.objects.get(card_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):

    cart = Cart.objects.get(card_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):

    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(card_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'cart.html', context)


def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by('-created_date')
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store.html', context)