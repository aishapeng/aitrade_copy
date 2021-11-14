from django import forms
from django.core.validators import EmailValidator


class ContactForm(forms.Form):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={
                               'class': "form-control",
                               'placeholder': 'Full Name'
                           }))
    email = forms.EmailField(required=True,
                             validators=[EmailValidator],
                             widget=forms.EmailInput(attrs={
                                 'class': "form-control",
                                 'placeholder': 'Email'
                             }))
    message = forms.CharField(required=True,
                              widget=forms.Textarea(attrs={
                                  'class': "form-control",
                                  'placeholder': 'Message'
                              }))

