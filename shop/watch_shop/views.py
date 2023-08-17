from django.contrib import messages
from django.contrib.auth import views as auth_views, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import View, DetailView, ListView, CreateView

from shop.watch_shop.forms import SignUpForm, CheckoutForm
from shop.watch_shop.models import Watch, Order, OrderWatch, Address


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


def home_view(request):
    return render(request, 'index.html')


class CatalogueView(ListView):
    model = Watch
    paginate_by = 6
    template_name = "shop.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class WatchDetail(DetailView):
    model = Watch
    template_name = "detail.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Watch, slug=slug)
    order_item, created = OrderWatch.objects.get_or_create(
        watch=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.watch.filter(watch__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order summary")
        else:
            order.watch.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.watch.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Watch, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.watch.filter(watch__slug=item.slug).exists():
            order_item = OrderWatch.objects.filter(
                watch=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("detail", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Watch, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.watch.filter(watch__slug=item.slug).exists():
            order_item = OrderWatch.objects.filter(
                watch=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("detail")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("detail", slug=slug)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_shipping_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_billing = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        billing_adress = address_qs[0]
                        order.shipping_address = billing_adress
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            billing_adress=billing_address1,
                            billing_address_alt=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order summary")

class SignUpView(CreateView):
    template_name = 'sign-up.html'
    form_class = SignUpForm
    success_url = reverse_lazy('catalogue')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        login(request, self.object)
        return response


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('home')


class SignInView(auth_views.LoginView):
    template_name = 'login.html'


def about_us_view(request):
    return render(request, 'about-us.html')
