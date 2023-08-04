from typing import Any, Dict
from django.shortcuts import redirect, render
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
)
from multi_form_view import MultiModelFormView
from django.contrib import messages
from django.http import JsonResponse

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
    ContactForm,
    ReviewForm,
    NewsLetterForm,
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

        filter_product_by_higher_views = filter_product_by_views.order_by(
            "-views_count")
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

        context["new_products_left_sidebar"] = products_by_date[:2]
        context["new_products_center"] = products_by_date[2]
        context["new_products_right_sidebar"] = products_by_date[3:5]

        context["featured_products"] = all_products.filter(is_featured=True)
        # context["default_active_tab_category"] = Category.objects.first()
        # context["remaining_categories"] = all_categories[1:8]

        return context


class ShopItemsView(HomePageView):
    model = Product
    template_name = "main/shop/shop.html"
    paginate_by = 3
    

class AboutUsPageView(TemplateView):
    template_name = "about_us.html"


class ContactUsPageView(TemplateView):
    template_name = "contact_us.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "main/home/product/product detail/product_details.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_products = Product.objects.all()
        current_product = Product.objects.get(slug=self.kwargs["slug"])

        current_product_category = current_product.category.name

        context["related_products"] = Product.objects.all().filter(
            category__name__icontains=current_product_category
        ).exclude(slug=current_product.slug)

        context["upsale_products"] = all_products.exclude(
            slug=current_product.slug)

        return context


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
            product = current_product
            return render(
                request,
                "main/home/product/product detail/product_details.html",
                {
                    "product": product,
                    "form": form
                }
            )


class ContactUsPageView(View):
    template_name = "contact_us.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        print(form)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Your message has been successfully sent—thank you for reaching out to us!"
            )
            return redirect("contact")
        else:
            messages.error(
                request, "Please ensure all required fields are filled out correctly \
                to submit the contact form."
            )
            return render(request, self.template_name, {"form": form})


class NewsLetterView(View):
    def post(self, request, *args, **kwargs):
        ajax_format = request.headers.get("x-requested-with")

        if ajax_format == "XMLHttpRequest":
            form = NewsLetterForm(request.POST)

            if form.is_valid():
                form.save()

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Thank you for subscribing to our electrifying newsletter! Get ready \
                                    for the latest tech trends, exclusive offers, expert tips, and \
                                    exciting giveaways as part of our electronic store community."
                    },
                    status=201
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Oops! It seems there was an issue with your newsletter \
                                    subscription—please double-check your email and try again."
                    },
                    status=400,
                )
        return JsonResponse(
            {
                'success': False,
                'message': 'Cannot process.Must be and AJAX XMLHttpRequest.',
            },
            status=400,
        )
