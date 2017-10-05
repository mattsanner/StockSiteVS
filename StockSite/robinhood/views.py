from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from . import forms
from .services import RobinhoodServices
from .models import RobinhoodUser

def register_or_login(request):
    if(request.user.is_authenticated and request.method == 'POST'):
        form = forms.RobinhoodRegistrationForm(request.POST)
        if(form.is_valid()):
            try:
                RobinhoodServices.authenticate(request.user, form.cleaned_data['username'], form.cleaned_data['password'])
                return HttpResponseRedirect(reverse('home'))
            except Exception as e:
                return render(request, 'robinhood/error.html', {'error_message': e})
    else:
        form = forms.RobinhoodRegistrationForm()
        try:
            request.user.robinhooduser            
            return render(request, 'robinhood/login.html', {'title': 'Log in to your Robinhood Account.', 'form': form})
        except RobinhoodUser.DoesNotExist as e:
            return render(request, 'robinhood/login.html', {'title': 'Log in to Robinhood to link your accounts.', 'form': form})
        except Exception as e:
            return render(request, 'robinhood/error.html', {'error_message': e})

def logout(request):
    if(request.user.is_authenticated):
        try:
            request.user.robinhooduser.signedin = False
            request.user.robinhooduser.token = b' '
            request.user.robinhooduser.save()
            return HttpResponseRedirect(reverse('home'))
        except RobinhoodUser.DoesNotExist as e:
            return render(request, 'robinhood/error.html', {'error_message': e})

#def registration(request):
#    if(request.user.is_authenticated and request.method == 'POST'):
#        form = forms.RobinhoodRegistrationForm(request.POST)
#        if(form.is_valid()):
#            try:
#                RobinhoodServices.authenticate(request.user, form.cleaned_data['username'], form.cleaned_data['password'])
#                return render(request, 'robinhood/success.html')
#            except Exception as e:
#                return render(request, 'robinhood/registration_error.html', {'error_message': e})
#    else:
#        form = forms.RobinhoodRegistrationForm()
    
    

#def robinhoodlogin(request):
#    if request.user.is_authenticated and request.method == 'POST':
#        form = forms.RobinhoodRegistrationForm(request.POST)
#        if(form.is_valid()):
#            try:
#                RobinhoodServices.authenticate(request.user, form.cleaned_data['username'], form.cleaned_data['password'])
#                return HttpResponseRedirect(template.Render())
#            except Exception as e:
#                return render(request, 'robinhood/login.html', {'title': 'Password or username was incorrect, try again', 'form': form})
#        else:
#            form = forms.RobinhoodRegistrationForm()
