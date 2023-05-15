from django.contrib import admin
from django import forms
from .models import User, Category, Listing, Comment, Bid


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)

# Disable comment requirement in admin panel when editing a listing
class ListingAdminForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'url', 'category']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    form = ListingAdminForm
