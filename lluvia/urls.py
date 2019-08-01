# params vs url best practices - https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get

from django.conf.urls import url
from . import views

urlpatterns = [
    # Calls like 'example.com' will match here and give the index page
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.spotify_login, name="spotify_login"),
    # address login denials
    url(r'^callback/$', views.process_login, name="process_login")
]
