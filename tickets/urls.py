from django.conf.urls import url, include
from tickets.views import ticket_index, create_ticket, edit_ticket, view_ticket, upvote_ticket
from django.views.generic import RedirectView


urlpatterns = [
    url(r'ticket_index/$', ticket_index, name='ticket_index') ,
    url(r'create_ticket/', create_ticket, name='create_ticket'),
    url(r'edit_ticket/(?P<id>\d+)$', edit_ticket, name='edit_ticket'),
    url(r'view_ticket/upvote_ticket/(?P<id>\d+)', upvote_ticket, name='upvote_ticket'),
    url(r'view_ticket/(?P<id>\d+)', view_ticket, name='view_ticket'),
 
]