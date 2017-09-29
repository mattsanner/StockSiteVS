from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^signin', views.robinhoodsignin, name='robinhood_signin'),
    url(r'^registration', views.registration, name='registration'),
    #url(r'^register', views.register)
]
