from django.contrib import admin
from .models import Ticket, TicketType, Comment

admin.site.register(Ticket)
admin.site.register(TicketType)
admin.site.register(Comment)