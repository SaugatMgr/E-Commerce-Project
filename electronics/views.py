from django.views.generic import (
    ListView,
    TemplateView,
)
from multi_form_view import MultiModelFormView


from .models import (
    Product,
    Image,
    Category,
    SubCategory,
)
from .forms import (
    AddProductForm,
    AddImagesForm,
)


class HomePageView(ListView):
    model = Product
    template_name = "main/home/home.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["product_category"] = Category.objects.all()[:9]
        context["product_category_rem"] = Category.objects.all()[9:12]
        context["product_sub_category"] = SubCategory.objects.all()

        return context


class AboutUsPageView(TemplateView):
    template_name = "about_us.html"


class ContactUsPageView(TemplateView):
    template_name = "contact_us.html"
