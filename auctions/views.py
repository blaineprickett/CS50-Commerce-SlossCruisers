from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from .models import Comment
from .forms import CreateListingForm

from .models import User
from .models import Listing
from .models import Bid
from .models import Comment
from decimal import Decimal



def index(request):
    listings = Listing.objects.filter(is_closed=False)
    context = {
        "listings": listings,
    }
    return render(request, "auctions/index.html", context)

def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_closed = True
    listing.save()
    return HttpResponseRedirect(reverse("display_listing", args=(listing_id, )))

def closed_listings(request):
    closed_listing = Listing.objects.filter(is_closed=True)
    context = {
        "listings": closed_listing,
    }
    return render(request, "auctions/closed_listing.html", context)

def display_category(request):
    category = request.POST.get("category")
    listings = Listing.objects.filter(category=category, is_closed=False)
    context = {
        "listings": listings,
        "category": category
    }
    return render(request, "auctions/category.html", context)

@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():
            listing = Listing(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                starting_bid=form.cleaned_data["price"],  # here we assign 'price' to 'starting_bid'
                category=form.cleaned_data["category"],
                url=form.cleaned_data["image_url"],
                owner=request.user,
            )
            listing.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            # The form is not valid, print out the errors to the console
            print(form.errors)
            # Convert the ErrorDict to a string and pass it to messages.error()
            messages.error(request, str(form.errors))

    else:
        form = CreateListingForm()

    return render(request, "auctions/create.html", {
        "form": form
    })

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}
        widgets = {'content': forms.Textarea(attrs={'cols': 80})}

def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.save()
            return HttpResponseRedirect(reverse("display_listing", args=[listing_id]))
    else:
        comment_form = CommentForm()

    # If the form is not valid, render the template with the form errors
    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "comments": Comment.objects.filter(listing=listing).order_by("-timestamp"),
        "comment_form": comment_form
    })


def create(request):
    # your code here
    return render(request, "auctions/create.html")


def display_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    comments = Comment.objects.filter(listing=listing).order_by("-timestamp")
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.listing = listing
            comment.user = request.user
            comment.save()
    else:
        comment_form = CommentForm()

    is_owner = listing.owner == request.user if request.user.is_authenticated else False

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "comments": comments,
        "comment_form": comment_form,
        "is_closed": listing.is_closed,
        "is_owner": is_owner,  # Add the is_owner field to the template context
    })


def foo(user: User):
    username = user.username

def display_watchlist(request):
        user = request.user
        listings = user.watch_listings.all()
        context = {
            "listings": listings,
        }

        return render(request, "auctions/watchlist_page.html", context)

def new_bid(request, listing_id):
    print(request.POST)
    listing = Listing.objects.get(pk=listing_id)
    print(listing) # Add this line to print the listing object
    current_bid = listing.current_bid or listing.opening_bid or Decimal(0)
    print(current_bid)  # Add this line to print the current_bid value
    new_bid = Decimal(request.POST["bid"])
    if new_bid > current_bid:
        updated_bid = Bid(bid=new_bid, user=request.user)
        updated_bid.save()
        listing.current_bid = new_bid
        listing.bids.add(updated_bid)
        listing.save()
        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "message": "Bid was updated successfully",
            "updated": True,
        })
    else:
        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "message": "Bid not high enough",
            "updated": False,
        })

         
def add_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("display_watchlist"))

def remove_watchlist(request, listing_id):
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        listing.watchlist.remove(user)

        return HttpResponseRedirect(reverse("display_listing", args=(listing_id, ))) 

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


