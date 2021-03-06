"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Username'}))
    email = forms.CharField(max_length=254,
                            widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Email'}))
    firstName = forms.CharField(max_length=30,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'First Name'}))
    password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                    'placeholder': 'Password'}))
    password2 = forms.CharField(label=_("Password confirmation"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Confirm Password'}))