from django.urls import path

from .views import (
    AddToWishListView,
    CheckOutView,
    UserAccountView,
    WishListView,
    remove_wishlist_item,
)

urlpatterns = [
    path("checkout/", CheckOutView.as_view(), name="checkout"),
    path("user-account/", UserAccountView.as_view(), name="user_account"),
    path("wishlist/", WishListView.as_view(), name="wishlist"),
    path("add-to-wishlist/", AddToWishListView.as_view(), name="add_to_wishlist"),
    path("remove-from-wishlist/", remove_wishlist_item, name="remove_from_wishlist"),
]
