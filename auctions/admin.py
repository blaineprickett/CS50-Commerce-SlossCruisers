from django.contrib import admin
from .models import User, Category, Listing, Comment, Bid

admin.site.register(User)
admin.site.register(Category)  # make sure to import the Category model
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
