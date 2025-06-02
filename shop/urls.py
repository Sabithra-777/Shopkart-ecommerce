from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
    path('cart', views.cart_page, name="cart"),
    path('wallet', views.wallet_page, name="wallet"),
    path('wallet/topup', views.wallet_topup, name="wallet_topup"),
    path('buy_now', views.buy_now, name="buy_now"),
    path('fav', views.favviewpage, name="favviewpage"),
    path('fav/ajax', views.fav_page, name="fav_page"),
    path('remove_cart/<str:cid>', views.remove_cart, name="remove_cart"),
    path('remove_fav/<str:fid>', views.remove_fav, name="remove_fav"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:name>', views.collectionsview, name="collections"),
    path('collections/<str:cname>/<str:pname>', views.product_details, name="product_details"),
    path('addtocart', views.add_to_cart, name="addtocart"),
]
