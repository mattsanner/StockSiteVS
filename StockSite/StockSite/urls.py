"""
Definition of urls for StockSite.
"""

from datetime import datetime
from django.contrib import admin
from django.conf.urls import url, include
import django.contrib.auth.views as authViews

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        authViews.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        authViews.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^robinhood/', include('robinhood.urls', namespace='robinhood'), name='robinhood'),
    url(r'^stock/(?P<stock>[a-zA-Z ]+)/', app.views.stock, name='single_stock'),
]