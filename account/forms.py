from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import Account

from binance import Client
from binance.exceptions import BinanceAPIException


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password', 'align': 'center', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'align': 'center',
                                          'placeholder': 'Password Confirmation'}),
    )
    secretKey = forms.CharField(
        label="Secret Key",
        widget=forms.TextInput(attrs={'class': 'form-control', 'align': 'center',
                                          'placeholder': 'Secret key'}),
    )

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2', 'publicKey', 'secretKey')
        labels = {
            'publicKey': 'Public Key',
            'secretKey': 'Secret Key'
        }
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'Email'
            }),
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
            }),
            'publicKey': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Public Key'
            }),
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        publicKey = self.cleaned_data.get('publicKey')
        secretKey = self.cleaned_data.get('secretKey')
        if Account.objects.filter(email=email).exists():
            raise ValidationError("Existing email account")
        if Account.objects.filter(publicKey=publicKey).exists():
            raise ValidationError("Binance API Key already registered")
        if Account.objects.filter(secretKey=secretKey).exists():
            raise ValidationError("Binance Secret Key already registered")
        if self.is_valid():
            try:
                apiKey = self.cleaned_data['publicKey']
                apiSecret = self.cleaned_data['secretKey']
                client = Client(apiKey, apiSecret)
                client.get_deposit_address(coin='BTC')
            except BinanceAPIException:
                raise ValidationError("Invalid Binance API/Secret Key")


class AccountAuthenthicationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password', 'align': 'center', 'placeholder': 'password'}),
    )

    class Meta:
        model = Account
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'Email'
            }),
        }

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")

