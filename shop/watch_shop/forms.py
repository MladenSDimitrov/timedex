from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2',)


class UserEditForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = "__all__"


class CheckoutForm(forms.Form):
    billing_address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'House number and street name'}))
    billing_address2 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Apartment, Suite, Unit, etc (optional)'}))
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Zip Code'}))
