from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.urls import reverse

from shop.watch_shop.managers import WatchShopUserManager
from shop.watch_shop.validators import validate_only_letters
from django_countries.fields import CountryField


class WatchShopUser(AbstractUser):
    MIN_LEN_FIRST_NAME = 2
    MAX_LEN_FIRST_NAME = 30
    MIN_LEN_LAST_NAME = 2
    MAX_LEN_LAST_NAME = 30

    first_name = models.CharField(
        max_length=MAX_LEN_FIRST_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LEN_FIRST_NAME),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=MAX_LEN_LAST_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LEN_LAST_NAME),
            validate_only_letters,
        )
    )

    email = models.EmailField(
        unique=True,
    )

    objects = WatchShopUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None


class Address(models.Model):
    user = models.ForeignKey(WatchShopUser, on_delete=models.CASCADE)
    billing_adress = models.CharField(max_length=100)
    billing_address_alt = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    @property
    def get_name(self):
        return self.user.email

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = 'Addresses'


class Watch(models.Model):
    name = models.CharField(max_length=40)
    watch_image = models.ImageField(upload_to="images/")
    price = models.FloatField()
    description = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add to cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove from cart", kwargs={
            'slug': self.slug
        })


class OrderWatch(models.Model):
    user = models.ForeignKey('WatchShopUser', on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    watch = models.ForeignKey('Watch', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.watch.name}"

    def get_total_item_price(self):
        return self.quantity * self.watch.price


class Order(models.Model):
    user = models.ForeignKey('WatchShopUser', on_delete=models.CASCADE)
    watch = models.ManyToManyField('OrderWatch')
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    received = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def get_total(self):
        total = 0
        for order_item in self.watch.all():
            total += order_item.get_total_item_price()
        return total


