from django import forms
from django.core.validators import validate_email

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=50)

class SignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=50)
    email = forms.CharField(label="Email", max_length=50, validators=[validate_email])

class CreateListingForm(forms.Form):
    header = forms.CharField(label="Title", max_length=100)
    skill = forms.CharField(label="Skill")
    skill_description = forms.CharField(label="Skill Description")
    price = forms.FloatField(label="Price")
    description = forms.CharField(label="Description")

class ReviewForm(forms.Form):
    header = forms.CharField(label="Title", max_length=50)
    text = forms.CharField(label="Review")
    rating = forms.FloatField(label="Rating")

class SearchForm(forms.Form):
    search_terms = forms.CharField(label="search_terms", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Search..', 'style':'border-radius:8px; margin-top:11px'}))
