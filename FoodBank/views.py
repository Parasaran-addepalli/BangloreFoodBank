from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Donation, Product, User, UserInfo, CorpInfo
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from cart.cart import Cart


# Create your views here.


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("FoodBank:main"))
        else:
            print("HEllo")
            return render(request, "firstpage.html")
    return render(request, "firstpage.html")


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        mobile = request.POST.get("phone")
        pan = request.POST.get("pan")
        user = User(username=username, password=password, email=email)
        user.set_password(user.password)
        user.save()
        userinfo = UserInfo(user=user, mobile=mobile, pan=pan)
        userinfo.save()
        return HttpResponseRedirect(reverse("FoodBank:main"))
    return render(request, "regindi.html")


def corp_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        # mobile = request.POST.get("phone")
        pan = request.POST.get("pan")
        tan = request.POST.get("tan")
        url = request.POST.get("url")
        user = User(username=username, password=password, email=email)
        user.set_password(user.password)
        user.save()

        userinfo = CorpInfo(user=user, pan=pan, tan=tan, url=url)
        userinfo.save()
        return HttpResponseRedirect(reverse("FoodBank:main"))
    return render(request, "regcorp.html")


@login_required
def main(request):
    products = Product.objects.all()
    return render(request, "Food-front.html", {"products": products})


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)


@login_required
def payment(request):
    currency = "INR"
    amount = 0  # Rs. 200
    # Create a Razorpay Order
    cart = Cart(request)
    for key, value in cart.cart.items():
        amount += int(value["price"]) * int(value["quantity"])
    print(amount * 10)
    amount *= 100
    razorpay_order = razorpay_client.order.create(
        dict(amount=amount, currency=currency, payment_capture="0")
    )

    # order id of newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = "paymenthandler/"

    # we need to pass these details to frontend.
    context = {}
    context["razorpay_order_id"] = razorpay_order_id
    context["razorpay_merchant_key"] = settings.RAZOR_KEY_ID
    context["razorpay_amount"] = amount
    context["currency"] = currency
    context["callback_url"] = callback_url

    return render(request, "cartSum.html", context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get("razorpay_payment_id", "")
            razorpay_order_id = request.POST.get("razorpay_order_id", "")
            signature = request.POST.get("razorpay_signature", "")
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # add cart to donations
                    cart = Cart(request)
                    for key, value in cart.cart.items():
                        d = Donation(
                            user=request.user,
                            product=value["product"],
                            quantity=value["quantity"],
                        )
                        d.save()
                    # render success page on successful caputre of payment
                    return render(request, "paymentsuccess.html")
                except:

                    # if there is an error while capturing payment.
                    return render(request, "paymentfail.html")
            else:
                print("hey")
                # if signature verification fails.
                return render(request, "paymentfail.html")
        except:
            print("hello")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()


@login_required()
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("FoodBank:main")


@login_required()
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required()
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("FoodBank:payment")


@login_required()
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("FoodBank:payment")


@login_required()
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required()
def cart_detail(request):
    return render(request, "cart/cart_detail.html")


def thank_you(request):
    return render(request, "thankyou.html")


def log_out(request):
    logout(request)
    return redirect("FoodBank:main")
