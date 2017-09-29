from django import forms

class RobinhoodRegistrationForm(forms.Form):
    username = forms.CharField(label='Username/Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)