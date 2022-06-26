from django.urls import path
from .views import (
    cart_add,
    corp_register,
    user_login,
    user_register,
    main,
    payment,
    item_clear,
    item_decrement,
    item_increment,
    cart_clear,
    cart_detail,
    thank_you,
    log_out,
)

app_name = "FoodBank"

urlpatterns = [
    path("", user_login, name="login"),
    path("register/", user_register, name="register"),
    path("register/corp", corp_register, name="corp_register"),
    path("main/", main, name="main"),
    path("payment/", payment, name="payment"),
    path("cart/add/<int:id>/", cart_add, name="cart_add"),
    path("cart/item_clear/<int:id>/", item_clear, name="item_clear"),
    path("cart/item_increment/<int:id>/", item_increment, name="item_increment"),
    path("cart/item_decrement/<int:id>/", item_decrement, name="item_decrement"),
    path("cart/cart_clear/", cart_clear, name="cart_clear"),
    path("cart/cart-detail/", cart_detail, name="cart_detail"),
    path("thank", thank_you, name="thank_you"),
    path("logout/", log_out, name="logout"),
]
