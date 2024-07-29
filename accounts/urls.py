from django.urls import path

from .views import (
    AddToWishListView,
    CheckOutView,
    EsewaPaymentVerifyView,
    EsewaPaymentView,
    KhaltiPaymentVerifyView,
    KhaltiPaymentView,
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
    path(
        "khalti-payment/<uuid:order_id>/",
        KhaltiPaymentView.as_view(),
        name="khalti_payment",
    ),
    path(
        "khalti-payment/verify/",
        KhaltiPaymentVerifyView.as_view(),
        name="khalti_payment_verify",
    ),
    path(
        "esewa-payment/<uuid:order_id>/",
        EsewaPaymentView.as_view(),
        name="esewa_payment",
    ),
    path(
        "esewa-payment/verify/<uuid:order_id>/",
        EsewaPaymentVerifyView.as_view(),
        name="esewa_payment_verify",
    ),
]
