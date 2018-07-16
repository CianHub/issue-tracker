from django.conf.urls import url, include
from payment.views import pay
from django.views.generic import RedirectView


urlpatterns = [
    url(r'pay/$', pay, name='pay'),
]