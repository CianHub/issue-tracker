from django.db import models
from tickets.models import Ticket, TicketType
from accounts.models import User

class PaymentInfo(models.Model):
    user = models.ForeignKey(User)
    full_name = models.CharField(max_length=200, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=40, blank=False)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.date_created, self.full_name)
    