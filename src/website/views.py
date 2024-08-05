import base64
import io

import stripe
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import OuterRef, Subquery, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from pdf2image import convert_from_path

from src.administration.admins.models import (
    Product, ProductVersion, Post, PostCategory, Order, Cart, OrderItem, OtherPlatform, Review
)
from src.administration.admins.forms import ReviewForm
from src.website.filters import ProductFilter, PostFilter
from src.website.forms import OrderForm
from src.website.models import BackgroundImage, DigitalPlatforms, Banner, ComingSoon, HomeSliderImage, FooterImage
from src.website.utility import total_amount, total_quantity

""" BASIC PAGES ---------------------------------------------------------------------------------------------- """


class HomeTemplateView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context['new_products'] = Product.objects.order_by('-created_on')[:10]
        context['blogs'] = Post.objects.order_by('-created_on')[:10]
        context['top'] = Product.objects.order_by('-sales', '-likes', )[:5]
        context['promotion'] = Product.objects.order_by('-sales', '-likes', ).first()
        context['slider'] = HomeSliderImage.objects.all()
        context['coming_soon'] = ComingSoon.objects.all()[:10]
        context['digital_platform'] = DigitalPlatforms.objects.all()
        banner = Banner.objects.all()
        context['banner'] = banner.order_by('-created_on').first()
        background = BackgroundImage.objects.all()
        context['background'] = background.order_by('-created_on').first()
        return context


class ContactUsTemplateView(TemplateView):
    template_name = 'website/contact_us.html'


class AboutUsTemplateView(TemplateView):
    template_name = 'website/about.html'


""" COMICS AND NOVELS PAGES ------------------------------------------------------------------------------------ """


class ProductListView(ListView):
    template_name = 'website/product_list.html'
    queryset = Product.objects.all()
    paginate_by = 24

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        sort = self.request.GET.get('sort')
        if sort == '1' and self.request is not None:
            product = Product.objects.order_by('created_on')
        elif sort == '2':
            lowest_price_subquery = ProductVersion.objects.filter(
                product=OuterRef('pk')
            ).order_by('price').values('price')[:1]

            product = Product.objects.annotate(
                lowest_price=Subquery(lowest_price_subquery)
            ).order_by('lowest_price')
        elif sort == '3':
            lowest_price_subquery = ProductVersion.objects.filter(
                product=OuterRef('pk')
            ).order_by('-price').values('price')[:1]

            product = Product.objects.annotate(
                lowest_price=Subquery(lowest_price_subquery)
            ).order_by('-lowest_price')
        else:
            product = Product.objects.all().order_by('-created_on')

        filter_product = ProductFilter(self.request.GET, queryset=product)
        paginator = Paginator(filter_product.qs, self.paginate_by)

        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context['products'] = page_obj
        context['total'] = paginator.num_pages
        context['filter_form'] = filter_product
        return context


# views.py


class ProductDetailView(DetailView):
    template_name = 'website/product_detail.html'
    model = Product
    pk_url_kwarg = "product_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = Product.objects.get(slug=self.kwargs['slug'])
        product.clicks += 1
        context['other_platform'] = OtherPlatform.objects.filter(product=product)
        context['related_product'] = Product.objects.filter(
            Q(categories__in=product.categories.all()) & ~Q(id=product.id)
        ).distinct()[:4]
        context['reviews'] = Review.objects.filter(product=product)
        context['form'] = ReviewForm(initial={'product': product})
        product.save()
        return context


from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect


@login_required()
def submit_review(request, slug):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            print('--------valiD')
            product = get_object_or_404(Product, slug=slug)
            review = form.save(commit=False)
            review.product = product  # Set product here
            review.user = request.user
            review.save()
            print('--------saved')
            return redirect('website:product-detail', slug=slug)
        else:
            print('--------invalid------------')
            print(form.errors)  # Print form errors to debug
    return redirect('website:product-detail', slug=slug)


""" ---------------- POST PAGES ------------------------------------------------------------------------------------ """


class PostListView(ListView):
    model = Post
    paginate_by = 24
    template_name = 'website/post_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        category = self.request.GET.get('category')

        if category and self.request is not None:
            post = Post.objects.filter(category__id=category)
        else:
            post = Post.objects.all().order_by('-created_on')

        context['recent'] = Post.objects.order_by('-created_on')[:5]
        context['popular_posts'] = Post.objects.order_by('-visits', '-read_time')[:5]
        filter_posts = PostFilter(self.request.GET, queryset=post)
        pagination = Paginator(filter_posts.qs, 24)
        page_number = self.request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        context['post_category'] = PostCategory.objects.all()
        context['posts'] = page_obj
        context['filter_form'] = filter_posts
        context['category'] = category
        return context


class PostDetailView(DetailView):
    template_name = 'website/post_detail.html'
    model = Post
    pk_url_kwarg = "post_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = Post.objects.get(slug=self.kwargs['slug'])
        post.visits += 1
        post.save()
        return context


""" ORDER AND CART  ------------------------------------------------------------------------------------------ """


@method_decorator(login_required, name='dispatch')
class CartTemplateView(TemplateView):
    template_name = 'website/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartTemplateView, self).get_context_data(**kwargs)
        context['cart'] = Cart.objects.filter(user=self.request.user)
        context['total_amount'] = total_amount(self.request)
        return context


@method_decorator(login_required, name='dispatch')
class AddToCart(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        version = request.POST.get('version_id')
        cart, created = Cart.objects.get_or_create(user=self.request.user, product_id=product_id,
                                                   product_version_id=version)
        if not created:
            cart.quantity += 1
        else:
            cart.quantity = 1
        cart.save()
        return redirect('website:cart')


@method_decorator(login_required, name='dispatch')
class IncrementCart(View):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        version = request.GET.get('version_id')
        cart = get_object_or_404(Cart, product_id=product_id, user=self.request.user, product_version_id=version)
        cart.quantity += 1
        cart.save()
        return redirect('website:cart')


@method_decorator(login_required, name='dispatch')
class DecrementCart(View):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        version = request.GET.get('version_id')
        cart = get_object_or_404(Cart, product_id=product_id, user=self.request.user, product_version_id=version)
        if str(cart.quantity) == "1":
            cart.delete()
            return redirect('website:cart')
        cart.quantity -= 1
        cart.save()
        return redirect('website:cart')


@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        version = request.GET.get('version_id')
        cart = get_object_or_404(Cart, product_id=product_id, user=self.request.user, product_version_id=version)
        cart.delete()
        return redirect('website:cart')


stripe.api_key = 'sk_test_51MzSVMKxiugCOnUxT0YN5E7M8BhbZrzPFrx6NE6vRwmkTIYKREvGTyLBfXhbdORJybRfmzVm2cjPBTkkuGyAjVfP00cf3sDcP9'


@method_decorator(login_required, name='dispatch')
class OrderCreate(View):

    def get(self, request):

        cart = Cart.objects.filter(user=self.request.user)
        amount = total_amount(self.request)
        context = {'form': OrderForm, 'cart': cart, 'total_amount': amount}
        return render(request, 'website/order.html', context)

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            payment = self.request.POST.get('payment')
            shipping = self.request.POST.get('shipping')
            if shipping == "normal":
                shipping_charges = 6
            else:
                shipping_charges = 10
            price = int(total_amount(request)) + shipping_charges
            line_items = []
            cart = Cart.objects.filter(user=self.request.user)
            qty = 0
            for product in cart:
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product.product_version.price * 100),
                        'product_data': {
                            'name': product.product.name,
                        },
                    },
                    "quantity": product.quantity
                })
                if product.product_version.version.name == 'Physical':
                    qty += 1
            for shipping in cart:
                print('loop')
                if shipping.product_version.version.name == 'Physical':
                    print('in')
                    line_items.append({
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(shipping_charges * 100),
                            'product_data': {
                                'name': 'Tax'
                            },
                        },
                        "quantity": '1'
                    })
                    break
            host = self.request.get_host()
            customer = stripe.Customer.create(
                name=self.request.user.username,
                email=self.request.user.email
            )
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer=customer,
                submit_type='pay',
                line_items=line_items,
                mode='payment',
                success_url='http://' + host + reverse('website:success') \
                            + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://' + host + reverse('website:cancel') \
                           + '?session_id={CHECKOUT_SESSION_ID}',

            )
            stripe_id = checkout_session['id']
            order = form.save(commit=False)
            order.user = self.request.user
            order.total = total_amount(request)
            order.stripe_payment_id = stripe_id
            if shipping == "normal":
                order.shipping = "Normal"
            elif shipping == "premium":
                order.shipping = "Premium"
            else:
                pass
            order.save()

            return redirect(checkout_session.url, code=303)
        else:
            form = OrderForm()
        return render(request, 'website/order.html', context={'form': OrderForm()})


@method_decorator(login_required, name='dispatch')
class SuccessPayment(View):
    def get(self, request, *args, **kwargs):
        stripe_id = self.request.GET.get('session_id')
        order = get_object_or_404(Order, user=self.request.user, stripe_payment_id=stripe_id)
        order.paid = order.total
        order.payment_status = 'completed'
        order.order_status = 'shipping'
        order.save()
        cart = Cart.objects.filter(user=self.request.user)
        for cart in cart:
            cart_item = OrderItem(product=cart.product, product_version=cart.product_version, order=order,
                                  qty=cart.quantity)
            cart_item.save()
            cart.delete()
        return render(self.request, 'website/success.html')


@method_decorator(login_required, name='dispatch')
class CancelPayment(View):
    template_name = 'website/cancel.html'

    def get(self, *args):
        stripe_id = self.request.GET.get('session_id')
        order = Order.objects.get(user=self.request.user, stripe_payment_id=stripe_id)
        order.delete()
        return render(self.request, template_name=self.template_name)


"""----------------------------ISSUES PAGES ------------------------------------------------------------------- """


class ReadSample(View):
    def get(self, request, pk, *args, **kwargs):
        pdf_file = Product.objects.get(id=pk)
        images = convert_from_path(pdf_file.book_file.path, first_page=1, last_page=15)

        image_data = []
        for image in images:
            with io.BytesIO() as output:
                image.save(output, format='PNG')
                image_data.append(base64.b64encode(output.getvalue()).decode('utf-8'))

        context = {'images': image_data}
        return render(request, 'client/sample_book.html', context)


class CookiePolicy(TemplateView):
    template_name = 'website/cookie_policy.html'


class PrivacyPolicy(TemplateView):
    template_name = 'website/privacy_policy.html'


class TermsAndCondition(TemplateView):
    template_name = 'website/terms_and_conditions.html'


class Jobs(TemplateView):
    template_name = 'website/jobs.html'


class ReturnPolicy(TemplateView):
    template_name = 'website/return_policy.html'


class ShippingPolicy(TemplateView):
    template_name = 'website/shipping_policy.html'
