from django.conf.urls import url, include
from tickets.views import ticket_index, create_ticket_type, edit_ticket, view_ticket, create_ticket_bug, create_ticket_feature, upvote_ticket
from django.views.generic import RedirectView


urlpatterns = [
    url(r'ticket_index/$', ticket_index, name='ticket_index') ,
    url(r'create_ticket/', create_ticket_type, name='create_ticket') ,
    url(r'create_ticket_bug_report/', create_ticket_bug, name='create_ticket_bug'),
    url(r'create_ticket_request_feature/', create_ticket_feature, name='create_ticket_feature'),
    url(r'edit_ticket/(?P<id>\d+)$', edit_ticket, name='edit_ticket'),
    url(r'view_ticket/upvote_ticket/(?P<id>\d+)', upvote_ticket, name='upvote_ticket'),
    url(r'view_ticket/(?P<id>\d+)', view_ticket, name='view_ticket'),
 
]