from django import forms
from .models import Comment
from .models import Listing

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}
        widgets = {'content': forms.Textarea(attrs={'cols': 80})}
        # Make the content field required
        required = {'content': False}

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'category', 'image_url']  # Ensure 'image_url' is in this list

