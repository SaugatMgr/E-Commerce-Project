from django.urls import path

from .views import (
    HomePageView,
    AboutUsPageView,
    ContactUsPageView,
    ProductDetailView,
    ProductSearchView,
    ReviewView,
    NewsLetterView,
    ShopItemsView,
    AddProductView,
    ProductUpdateView,
    ProductDeleteView,
    AddProductToCartView,
    ShowCartItemsView,
    remove_cart_item,
    update_cart_item_quantity,
)

urlpatterns = [
    # different pages url
    path("", HomePageView.as_view(), name="home"),
    path("shop/", ShopItemsView.as_view(), name="shop"),
    path(
        "category/<str:category_name>/<int:category_id>/",
        ShopItemsView.as_view(),
        name="product_by_category",
    ),
    path(
        "sub-category/<str:sub_category_name>/<int:sub_category_id>/",
        ShopItemsView.as_view(),
        name="product_by_sub_category",
    ),
    path("shop/<int:tag_id>/", ShopItemsView.as_view(), name="product_by_tag"),
    path("about/", AboutUsPageView.as_view(), name="about"),
    path("contact/", ContactUsPageView.as_view(), name="contact"),
    # product detail url
    path(
        "product-detail/<slug:slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    # product review url
    path("review/", ReviewView.as_view(), name="review"),
    # newsletter url
    path("newsletter/", NewsLetterView.as_view(), name="newsletter"),
    # url for CRUD operations on Product
    path("create/", AddProductView.as_view(), name="add_product"),
    path("update/<slug:slug>/", ProductUpdateView.as_view(), name="update_product"),
    path("delete/<slug:slug>/", ProductDeleteView.as_view(), name="delete_product"),
    # Add to Cart
    path("cart/", ShowCartItemsView.as_view(), name="cart"),
    path("add-to-cart/", AddProductToCartView.as_view(), name="add_to_cart"),
    path("update-cart/", update_cart_item_quantity, name="update_cart"),
    path("remove-from-cart/", remove_cart_item, name="remove_from_cart"),
    # Search
    path("search/", ProductSearchView.as_view(), name="search"),
]
