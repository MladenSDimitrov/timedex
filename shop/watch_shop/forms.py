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

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

