from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail

from addresses.forms import AddressForm
from addresses.models import Address

from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart
import juspayp3



def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
            "id": x.id,
            "url": x.get_absolute_url(),
            "name": x.name, 
            "price": x.price
            } 
            for x in cart_obj.products.all()]
    cart_data  = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj,
                                                "billing_profile": billing_profile})


def cart_update(request):
    product_id = request.POST.get('product_id')
    
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj) 
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data, status=200) 
    return redirect("cart:home")


def checkout_home(request):
    context = dict()
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")  
    
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id) 
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    c = juspayp3.Orders.create(
        order_id=order_obj.order_id,
        amount=order_obj.total,
        customer_id=billing_profile.customer_id,
        customer_email=billing_profile.email,
        customer_phone='9988665522',
        return_url='http://127.0.0.1:8000/cart/checkout/success/'
    )
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "link": c.payment_links.web
    }
    return render(request, "carts/checkout.html", context)

def checkout_handle_view(request):
    resp_dict = dict()
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

    resp_dict['order_id'] = request.GET.get('order_id')
    resp_dict['status'] = request.GET.get('status')
    resp_dict['signature'] = request.GET.get('signature')
    resp_dict['signature_algorithm'] = request.GET.get('signature_algorithm')

    print(resp_dict['status'])

    if resp_dict['status'] == 'CHARGED':
        order_obj.mark_paid()
        request.session['cart_items'] = 0
        del request.session['cart_id']
        return redirect("cart:success")
    else:
        print('Opps! an error.')
        return redirect("cart:success")

    return render(request, 'carts/response.html', resp_dict)

def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})