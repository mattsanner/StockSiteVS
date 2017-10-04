from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    #TODO look into having two paths lead to same view, or refactor pathing
    url(r'^signin', views.register_or_login, name='login'),
    url(r'^registration', views.register_or_login, name='registration'),
    url(r'^logout', views.logout, name='logout')
    #url(r'^register', views.register)
]
