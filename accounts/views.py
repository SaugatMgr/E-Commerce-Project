from django.views.generic import CreateView

from .forms import CheckOutForm

class CheckOutView(CreateView):
    template_name = "users/checkout.html"
    form_class = CheckOutForm