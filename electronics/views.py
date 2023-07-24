from django.views.generic import ListView, TemplateView

from .models import Electronics


class HomePageView(ListView):
    model = Electronics
    template_name = "main/home/home.html"


class AboutUsPageView(TemplateView):
    template_name = "about_us.html"


class ContactUsPageView(TemplateView):
    template_name = "contact_us.html"
