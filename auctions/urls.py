from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.display_listing, name="display_listing"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/new_bid", views.new_bid, name="new_bid"),
    path("<int:listing_id>/add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("<int:listing_id>/remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("display_watchlist", views.display_watchlist, name="display_watchlist"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("<int:listing_id>/close_auction", views.close_auction, name="close_auction"),
    path("display_category", views.display_category, name="display_category"),
]   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




