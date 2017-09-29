from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from . import forms
from .services import RobinhoodServices

def registration(request):
    if(request.user.is_authenticated and request.method == 'POST'):
        form = forms.RobinhoodRegistrationForm(request.POST)
        if(form.is_valid()):
            try:
                RobinhoodServices.register(request.user, form.cleaned_data['username'], form.cleaned_data['password'])                
                return render(request, 'robinhood/success.html')
            except Exception as e:
                return render(request, 'robinhood/registration_error.html', {'error_message': e})
    else:
        form = forms.RobinhoodRegistrationForm()
    
    return render(request, 'robinhood/signin.html', {'title': 'Sign in to Robinhood to link your accounts.', 'form': form})

def robinhoodsignin(request):
    #if request.user.is_authenticated:
    #    template = loader.get_template("robinhood/signin.html")
    #    return HttpResponse(template.render())
    #else:
    #    return redirect(reverse('account_login'))
    if request.user.is_authenticated and request.method == 'POST':
        form = forms.RobinhoodRegistrationForm(request.POST)
        if(form.is_valid()):
            try:
                RobinhoodServices.authenticate(request.user, form.cleaned_data['username'], form.cleaned_data['password'])
                template = loader.get_template("robinhood/success.html")
                return HttpResponseRedirect(template.Render())
            except Exception as e:
                return render(request, 'robinhood/signin.html', {'title': 'Password or username was incorrect, try again', 'form': form})
        else:
            form = forms.RobinhoodRegistrationForm()
        return render(request, 'robinhood/signin.html', {'title': 'Sign in to your Robinhood Account.', 'form': form})