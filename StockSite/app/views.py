"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from robinhood.models import RobinhoodUser
from robinhood.services import RobinhoodServices

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)    
    try:
        request.user.robinhooduser
        has_robinhood = True
        rh_signedin = request.user.robinhooduser.signedin
    except (RobinhoodUser.DoesNotExist, AttributeError) as e:
        has_robinhood = False
        rh_signedin = False   

    stockList = RobinhoodServices.get_stocks(request.user)

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'has_robinhood': has_robinhood,
            'rh_loggedin': rh_signedin,
            'stock_list': stockList,
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
