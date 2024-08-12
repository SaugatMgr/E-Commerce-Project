from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
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

from helpers.pagination import PaginationMixin

from .models import (
    Category,
    Product,
    Image,
    Rating,
    Review,
    SubCategory,
)
from accounts.models import (
    Customer,
    Cart,
    CartItems,
    WishList,
)
from .forms import (
    AddProductForm,
    ContactForm,
    ReviewForm,
    NewsLetterForm,
)


class HomePageView(PaginationMixin, ListView):
    model = Product
    template_name = "main/home/home.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_categories = Category.objects.all()
        all_products = Product.objects.all()
        filter_product_by_views = Product.objects.filter(views_count__gte=0)
        filter_product_by_higher_views = filter_product_by_views.order_by(
            "-views_count"
        )
        products_by_date = filter_product_by_views.order_by("-added_date")

        context["product_category"] = all_categories[:9]
        context["product_category_rem"] = all_categories[9:12]
        context["product_sub_category"] = SubCategory.objects.all()

        context["today_deals_categories"] = all_categories[:7]

        context["best_sellers"] = filter_product_by_higher_views
        context["all_products"] = all_products

        context["new_products_left_sidebar"] = products_by_date[:2]
        context["new_products_center"] = products_by_date[2]
        context["new_products_right_sidebar"] = products_by_date[3:5]

        context["featured_products"] = all_products.filter(is_featured=True)
        context["home_product_area_categories"] = all_categories[:7]

        return context


class ShopItemsView(PaginationMixin, ListView):
    model = Product
    template_name = "main/shop/shop.html"
    paginate_by = 12

    def get_queryset(self):
        get_data = self.request.GET
        kwargs_data = self.kwargs
        queryset = Product.objects.all()

        order_by = get_data.get("orderby")
        filter_by_price_range = get_data.get("text")
        category_id = kwargs_data.get("category_id")
        sub_category_id = kwargs_data.get("sub_category_id")
        tag_id = kwargs_data.get("tag_id")

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if sub_category_id:
            queryset = queryset.filter(sub_category__id=sub_category_id)
        if tag_id:
            queryset = queryset.filter(tag__id=tag_id).distinct()
        if order_by:
            queryset = queryset.order_by(order_by)
        if filter_by_price_range:
            filter_by_price_range = filter_by_price_range.replace("Rs.", "")
            min_price, max_price = filter_by_price_range.split(" - ")
            min_price = int(min_price)
            max_price = int(max_price)
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset

    def get(self, request, *args, **kwargs):
        get_data = request.GET
        paginator, page_obj, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(), self.paginate_by
        )
        ajax_format = request.headers.get("x-requested-with")
        order_by = get_data.get("orderby", "")
        filter_by_price_range = get_data.get("text", "")

        if ajax_format:
            if ajax_format == "XMLHttpRequest":
                if order_by:
                    html_content = render_to_string(
                        "main/shop/right side/right_side.html",
                        {
                            "page_obj": page_obj,
                            "is_paginated": page_obj.has_other_pages(),
                        },
                        request,
                    )
                    return JsonResponse(
                        {"success": True, "html_content": html_content}, status=200
                    )
                if filter_by_price_range:
                    html_content = render_to_string(
                        "main/shop/right side/right_side.html",
                        {
                            "page_obj": page_obj,
                            "is_paginated": page_obj.has_other_pages(),
                        },
                        request,
                    )
                    return JsonResponse(
                        {"success": True, "html_content": html_content}, status=200
                    )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                    },
                    status=400,
                )
        return super().get(request, *args, **kwargs)


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
        data = request.POST
        form = ReviewForm(data)
        product_id = data["product"]
        current_product = Product.objects.get(pk=product_id)

        if form.is_valid():
            form = Review(
                name=data["name"],
                email=data["email"],
                msg=data["msg"],
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
                    data = request.POST
                    product_slug = data.get("prod_slug")
                    req_from_wishlist = data.get("wish_list_add_to_cart")
                    user = self.request.user
                    product = Product.objects.get(slug=product_slug)
                    customer, created = Customer.objects.get_or_create(user=user)
                    cart, created = Cart.objects.get_or_create(customer=customer)
                    extra_message = {
                        "wish_list_prod_removed": True,
                    }

                    if req_from_wishlist == "true":
                        wish_list = WishList.objects.get(customer=customer)
                        wish_list.product.remove(product)

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

                            data = {
                                "success": True,
                                "message": f"You added {product.name} {get_matching_cart_product.quantity} times.",
                                "cart_update_html_content": render_to_string(
                                    template_name="users/shopping_cart.html",
                                    request=request,
                                ),
                            }
                            if req_from_wishlist == "true":
                                data.update(extra_message)

                            return JsonResponse(
                                data,
                                status=201,
                            )
                        else:
                            CartItems.objects.create(cart=cart, product=product)
                            data = {
                                "success": True,
                                "message": f"{product.name} added to cart successfully.",
                                "cart_update_html_content": render_to_string(
                                    template_name="users/shopping_cart.html",
                                    request=request,
                                ),
                            }
                            if req_from_wishlist == "true":
                                data.update(extra_message)

                            return JsonResponse(
                                data,
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


@require_POST
def update_cart_item_quantity(request):
    ajax_format = request.headers.get("x-requested-with")

    with transaction.atomic():
        if ajax_format == "XMLHttpRequest":
            data = request.POST
            product_slugs = data.getlist("prod_slug")
            new_quantities = data.getlist("quantity")

            if len(product_slugs) == len(new_quantities):
                user = request.user
                customer = Customer.objects.get(user=user)
                cart = Cart.objects.get(customer=customer)

                products = Product.objects.filter(slug__in=product_slugs)
                cart_items = CartItems.objects.filter(cart=cart, product__in=products)

                cart_items_with_new_quantity = zip(cart_items, new_quantities)
                for cart_item, quantity in cart_items_with_new_quantity:
                    cart_item.quantity = quantity
                CartItems.objects.bulk_update(cart_items, ["quantity"])

                updated_cart_items = [
                    {"prod_slug": item.product.slug, "quantity": item.quantity}
                    for item in cart_items
                ]

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Cart updated successfully.",
                        "updated_cart_items": updated_cart_items,
                    },
                    status=200,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Product slug and quantity must be provided.",
                    },
                    status=400,
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
        cart_items = CartItems.objects.filter(cart=cart)

        context["user_cart_items"] = cart_items
        context["cart_item_count"] = 0 if not cart_items else cart_items.count()

        return context


@require_POST
def remove_cart_item(request):
    ajax_format = request.headers.get("x-requested-with")

    with transaction.atomic():
        if ajax_format == "XMLHttpRequest":
            product_slug = request.POST.get("prod_slug")
            if product_slug:
                product = Product.objects.get(slug=product_slug)
                customer = Customer.objects.get(user=request.user)

                cart = Cart.objects.get(customer=customer)
                cart_item = CartItems.objects.get(cart=cart, product=product)
                cart_item.delete()

                return JsonResponse(
                    {
                        "success": True,
                        "message": f"{product.name} removed from your cart.",
                    },
                    status=200,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                },
                status=400,
            )


class ProductSearchView(View):
    model = Product
    template_name = "main/search/search_results.html"

    def get(self, request, *args, **kwargs):
        get_data = request.GET
        query = get_data.get("query", "")
        category_id = get_data.get("select", 0)
        orderby = get_data.get("orderby", "")
        filter_by_price_range = get_data.get("text", "")
        ajax_format = request.headers.get("x-requested-with")

        search_results = Product.objects.all()
        if query:
            search_results = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        if category_id:
            category_id = int(category_id)
            if category_id > 0:
                search_results = search_results.filter(category__id=category_id)

        search_results = search_results.order_by("-added_date")

        if orderby:
            search_results = search_results.order_by(orderby)

        if filter_by_price_range:
            filter_by_price_range = filter_by_price_range.replace("Rs.", "")
            min_price, max_price = filter_by_price_range.split(" - ")
            min_price = int(min_price)
            max_price = int(max_price)

            search_results = search_results.filter(
                price__gte=min_price, price__lte=max_price
            )

        page_obj = Paginator(search_results, 12)
        page = request.GET.get("page", 1)

        try:
            page_obj = page_obj.page(page)
        except PageNotAnInteger:
            page_obj = page_obj.page(1)
        except EmptyPage:
            page_obj = page_obj.page(page_obj.num_pages)

        if ajax_format:
            if ajax_format == "XMLHttpRequest":
                if orderby:
                    html_content = render_to_string(
                        self.template_name,
                        {
                            "query": query,
                            "page_obj": page_obj,
                            "is_paginated": page_obj.has_other_pages(),
                        },
                        request,
                    )
                    return JsonResponse(
                        {"success": True, "html_content": html_content}, status=200
                    )
                if filter_by_price_range:
                    html_content = render_to_string(
                        self.template_name,
                        {
                            "query": query,
                            "page_obj": page_obj,
                            "is_paginated": page_obj.has_other_pages(),
                        },
                        request,
                    )
                    return JsonResponse(
                        {"success": True, "html_content": html_content}, status=200
                    )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                    },
                    status=400,
                )
        return render(
            request,
            self.template_name,
            {
                "query": query,
                "page_obj": page_obj,
                "is_paginated": page_obj.has_other_pages(),
            },
        )


class ProductRatingView(View):
    def post(self, request, *args, **kwargs):
        ajax_format = request.headers.get("x-requested-with")

        if ajax_format == "XMLHttpRequest":
            data = request.POST
            product_id = data.get("product_id")
            rating = data.get("rating")
            user = request.user

            product = Product.objects.get(pk=product_id)

            if rating:
                rating = int(rating)
                existing_rating_by_user = Rating.objects.filter(
                    product=product, user=user
                )

                if rating == 0 and existing_rating_by_user.exists():
                    existing_rating_by_user.delete()
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Rating removed successfully.",
                        },
                        status=200,
                    )
                user_rating, created = Rating.objects.update_or_create(
                    product=product, user=user, defaults={"rating": rating}
                )
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Product rated successfully.",
                    },
                    status=201,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Rating must be provided.",
                    },
                    status=400,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                },
                status=400,
            )
