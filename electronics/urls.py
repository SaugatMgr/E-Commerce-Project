from django.urls import path

from .views import(
    HomePageView,
    AboutUsPageView,
    ContactUsPageView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutUsPageView.as_view(), name="about"),
    path("contact/", ContactUsPageView.as_view(), name="contact"),
]
