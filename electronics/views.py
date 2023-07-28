from django.shortcuts import redirect, render
from django.views.generic import (
    View,
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
    Review,
    Contact,
)
from .forms import (
    AddProductForm,
    AddImagesForm,
    ReviewForm,
)


class HomePageView(ListView):
    model = Product
    template_name = "main/home/home.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_categories = Category.objects.all()
        
        all_products = Product.objects.all()
        filter_product_by_views = Product.objects.filter(views_count__gte=0)
        
        filter_product_by_higher_views = filter_product_by_views.order_by("-views_count")
        products_by_date = filter_product_by_views.order_by("-added_date")
            
        context["categories"] = all_categories
        context["product_category"] = all_categories[:9]
        context["product_category_rem"] = all_categories[9:12]
        context["product_sub_category"] = SubCategory.objects.all()

        context["today_deals_categories_first"] = all_categories.first()
        context["today_deals_categories"] = all_categories[1:8]
        context["today_deals_products"] = products_by_date

        context["best_sellers"] = filter_product_by_higher_views
        context["all_products"] = all_products
        
        return context


class AboutUsPageView(TemplateView):
    template_name = "about_us.html"


class ContactUsPageView(TemplateView):
    template_name = "contact_us.html"

class ProductDetailView(DetailView):
    model = Product
    template_name = "main/home/product/product detail/product_details.html"
    context_object_name = "product"
    
class ReviewView(View):
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        product_id = request.POST["product"]
        current_product = Product.objects.get(pk=product_id)
        
        if form.is_valid():
            form = Review(
                name=request.POST["name"],
                email=request.POST["email"],
                msg=request.POST["msg"],
                user=self.request.user,
                product=current_product
            )
            form.save()
            return redirect("product_detail", current_product.slug)
        else:
            product=current_product
            return render(
                request,
                "main/home/product/product detail/product_details.html",
                {
                    "product": product,
                    "form": form
                }
            )
            