from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
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

        all_categories = Category.objects.all()
        filter_product = Product.objects.filter(views_count__gte=0).order_by("-views_count")
             
        context["categories"] = all_categories
        context["product_category"] = all_categories[:9]
        context["product_category_rem"] = all_categories[9:12]
        context["product_sub_category"] = SubCategory.objects.all()

        context["best_sellers"] = filter_product
        
        return context


class AboutUsPageView(TemplateView):
    template_name = "about_us.html"


class ContactUsPageView(TemplateView):
    template_name = "contact_us.html"

class ProductDetailView(DetailView):
    model = Product
    template_name = "main/home/product/product detail/product_details.html"
    context_object_name = "product"
    