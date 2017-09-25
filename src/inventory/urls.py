from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^add$', views.Add.as_view(), name='index'),
]
