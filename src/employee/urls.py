from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^profile$', views.Profile.as_view(), name='profile'),
    url(r'^change$', views.Change.as_view(), name='change'),
    url(r'^password$', views.Password.as_view(), name='password'),
]
