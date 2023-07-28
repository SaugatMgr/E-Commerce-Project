from django.urls import path

from .views import(
    HomePageView,
    AboutUsPageView,
    ContactUsPageView,
    ProductDetailView,
    ReviewView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutUsPageView.as_view(), name="about"),
    path("contact/", ContactUsPageView.as_view(), name="contact"),
    path("product-detail/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("review/", ReviewView.as_view(), name="review"),
]
