from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction

from .models import (
    Product,
    Image,
    Category,
    SubCategory,
    Review,
)
from accounts.models import (
    Customer,
    Cart,
    CartItems,
)
from .forms import (
    AddProductForm,
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

        user = self.request.user
        all_categories = Category.objects.all()
        all_products = Product.objects.all()

        filter_product_by_views = Product.objects.filter(views_count__gte=0)
        filter_product_by_higher_views = filter_product_by_views.order_by(
            "-views_count"
        )
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

        if user.is_authenticated:
            current_customer = Customer.objects.filter(user=user).first()
            if current_customer:
                cart = Cart.objects.filter(customer=current_customer).first()
                if cart:
                    cart_items = CartItems.objects.filter(cart=cart)
                    if cart_items:
                        context["cart_items"] = cart_items
                        context["cart_items_count"] = cart_items.count()
                        context["sub_total"] = sum(
                            [item.quantity * item.product.price for item in cart_items]
                        )

        return context


class ShopItemsView(HomePageView):
    model = Product
    template_name = "main/shop/shop.html"
    paginate_by = 3


class AboutUsPageView(TemplateView):
    template_name = "about_us.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "main/home/product/product detail/product_details.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_products = Product.objects.all()
        current_product = Product.objects.get(slug=self.kwargs["slug"])

        current_product_category = current_product.category.name

        context["related_products"] = (
            Product.objects.all()
            .filter(category__name__icontains=current_product_category)
            .exclude(slug=current_product.slug)
        )

        context["upsale_products"] = all_products.exclude(slug=current_product.slug)

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
                product=current_product,
            )
            form.save()
            return redirect("product_detail", current_product.slug)
        else:
            product = current_product
            return render(
                request,
                "main/home/product/product detail/product_details.html",
                {"product": product, "form": form},
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
                request,
                "Your message has been successfully sent—thank you for reaching out to us!",
            )
            return redirect("contact")
        else:
            messages.error(
                request,
                "Please ensure all required fields are filled out correctly \
                to submit the contact form.",
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
                                    exciting giveaways as part of our electronic store community.",
                    },
                    status=201,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Oops! It seems there was an issue with your newsletter \
                                    subscription—please double-check your email and try again.",
                    },
                    status=400,
                )
        return JsonResponse(
            {
                "success": False,
                "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
            },
            status=400,
        )


class AddProductView(CreateView):
    template_name = "product/add_product.html"
    form_class = AddProductForm

    def form_valid(self, form):
        product_object = form.save()  # AddProductForm lai save garne
        more_product_images = self.request.FILES.getlist("images")

        for img in more_product_images:
            Image.objects.create(product=product_object, images=img)

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = AddProductForm
    template_name = "product/update_product.html"

    def form_valid(self, form):
        product_object = form.save()  # AddProductForm lai save garne
        more_product_images = self.request.FILES.getlist("images")

        for img in more_product_images:
            Image.objects.create(product=product_object, images=img)

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product/delete_product.html"
    context_object_name = "product"
    success_url = reverse_lazy("home")


class AddProductToCartView(View):
    def post(self, request, *args, **kwargs):
        ajax_format = request.headers.get("x-requested-with")

        with transaction.atomic():
            if ajax_format == "XMLHttpRequest":
                if self.request.user.is_authenticated:
                    product_slug = request.POST["prod_slug"]
                    user = self.request.user

                    product = Product.objects.get(slug=product_slug)
                    customer, created = Customer.objects.get_or_create(user=user)
                    cart, created = Cart.objects.get_or_create(customer=customer)

                    # Check if the product exists
                    if product:
                        # Check if product is already in the cart
                        product_already_in_cart = CartItems.objects.filter(
                            cart=cart, product=product
                        )

                        if product_already_in_cart:
                            get_matching_cart_product = CartItems.objects.get(
                                cart=cart, product=product
                            )
                            get_matching_cart_product.quantity += 1
                            get_matching_cart_product.save()

                            return JsonResponse(
                                {
                                    "success": True,
                                    "message": f"You added {product.name} {get_matching_cart_product.quantity} times.",
                                },
                                status=201,
                            )
                        else:
                            CartItems.objects.create(cart=cart, product=product)
                            return JsonResponse(
                                {
                                    "success": True,
                                    "message": f"{product.name} added to cart successfully.",
                                },
                                status=201,
                            )
                    else:
                        return JsonResponse(
                            {
                                "success": False,
                                "message": "The product does not exist.",
                            },
                            status=400,
                        )
                else:
                    return JsonResponse(
                        {"success": False, "message": "Please Login to continue..."},
                        status=401,
                    )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                    },
                    status=400,
                )


class ShowCartItemsView(ListView):
    model = CartItems
    template_name = "users/shopping_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        customer = Customer.objects.get(user=user)
        cart = Cart.objects.get(customer=customer)

        context["user_cart_items"] = CartItems.objects.filter(cart=cart)

        return context
