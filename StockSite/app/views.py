"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from robinhood.models import RobinhoodUser

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)    
    try:
        request.user.robinhooduser
        has_robinhood = True
    except RobinhoodUser.DoesNotExist as e:
        has_robinhood = False
    except AttributeError as e:
        has_robinhood = False

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'has_robinhood': has_robinhood,
        }
    )

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
