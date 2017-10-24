"""
Definition of views.
"""

from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.validators import validate_email, ValidationError
from datetime import datetime
from robinhood.models import RobinhoodUser
from robinhood.services import RobinhoodServices
from app.util import json_encode_decimal

from . import forms
import json

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest) 
    if(request.user.is_authenticated):
        try:
            request.user.robinhooduser
            has_robinhood = True
            rh_signedin = request.user.robinhooduser.signedin
            if(rh_signedin):
                stockList = RobinhoodServices.get_stocks(request.user)
            else:
                stockList = ""
        except (RobinhoodUser.DoesNotExist, AttributeError) as e:
            has_robinhood = False
            rh_signedin = False   
            stockList = ""    

        return render(
            request,
            'app/index.html',
            {
                'title':'Stock Dashboard',
                'year':datetime.now().year,
                'has_robinhood': has_robinhood,
                'rh_loggedin': rh_signedin,
                'stock_list': stockList,
                'stock_json': json.dumps(stockList, default=json_encode_decimal),
            }
        )
    else:
        return redirect('login');

#Need to add authentication checks, pass in RH user, etc.
def stock(request, stock):
    assert isinstance(request, HttpRequest)
    stockContext = RobinhoodServices.get_user_stock_info(request.user, stock.upper())
    return render(
        request,
        'app/stock.html',
        {
            'title': 'Stock Dashboard',
            'stock_info': stockContext[0],
            'user_stake': stockContext[1],
        }
    )

def create_user(request):
    if(request.method == 'POST'):
        form = forms.RegistrationForm(request.POST)
        if(form.is_valid() and form.cleaned_data['password1'] == form.cleaned_data['password2']):
            try:
                validate_email(form.cleaned_data['email']);
                user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
                user.first_name = form.cleaned_data['firstName']
                user.save()
                return HttpResponseRedirect(reverse('login'))
            except ValidationError as e:                
                return render(request, 'app/user_registration.html', {'title': 'Enter a valid email address', 'form': forms.RegistrationForm()})
            except Exception as e:
                return render(request, 'app/user_registration.html', {'title': 'There was an error processing your submission. Try again.', 'form': forms.RegistrationForm()})
        else:
            return render(request, 'app/error.html', {'error': 'Form data was not valid and/or passwords did not match' })
    else:
        form = forms.RegistrationForm()
        return render(request, 'app/user_registration.html', {'title': 'Create a User', 'form': form})

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
