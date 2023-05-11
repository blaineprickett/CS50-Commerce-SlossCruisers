from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import AppConfig
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.apps import AppConfig
from django.db.models import BigAutoField
from django.contrib import admin
from decimal import Decimal


class AuctionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auctions'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()


class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bid} from {self.user}"


class Listing(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", null=True, blank=True)
    is_closed = models.BooleanField(default=False, blank=True, null=True)
    description = models.CharField(max_length=2000)
    opening_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    url = models.CharField(max_length=800)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watch_listings")
    category = models.CharField(max_length=400, null=True, blank=True)
    comments = models.ManyToManyField('Comment', related_name="listings_comments")
    bids = models.ManyToManyField(Bid, related_name="listings_bids", blank=True)
    content = models.TextField(default='default content')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.CharField(max_length=900, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)

    def __str__(self):
        return f"{self.title}: {self.current_bid}"

    def get_bid_status(self):
        if self.current_bid is None:
            return "Starting Bid: "
        else:
            return "Current Bid: "

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.user.username} on {self.listing.title}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
