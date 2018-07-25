from django.db import models
from django.utils import timezone
from tickets.models import Ticket

class Ticket_Time(models.Model):
    # Model that stores ticket data relevent to graphs
    
    ticket = models.ForeignKey(Ticket)
    match_ticket_id = models.IntegerField()
    date_started = models.DateTimeField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)

    def __int__(self):
        return self.match_ticket_id
