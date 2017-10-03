from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^faq$', views.Faq.as_view(), name='faq'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),
    url(r'^error$', views.Error.as_view(), name='error'),

]
