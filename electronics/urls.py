from django.urls import path

from .views import(
    HomePageView,
    AboutUsPageView,
    ContactUsPageView,
    ProductDetailView,
    ReviewView,
    NewsLetterView,
    ShopItemsView,
    AddProductView,
    ProductUpdateView,
    ProductDeleteView,
    AddProductToCartView,
    ShowCartItemsView,
)

urlpatterns = [
    # different pages url
    path("", HomePageView.as_view(), name="home"),
    path("shop/", ShopItemsView.as_view(), name="shop"),
    path("about/", AboutUsPageView.as_view(), name="about"),
    path("contact/", ContactUsPageView.as_view(), name="contact"),
    # product detail url
    path("product-detail/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
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
]
