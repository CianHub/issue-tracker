from django.conf.urls import url, include
from .views import charts
from django.views.generic import RedirectView

urlpatterns = [
    url(r'charts/$', charts, name='charts') ,
]