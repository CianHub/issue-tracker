from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Ticket(models.Model):
    # The model for a ticket 
    
    STATUS_CHOICES = (
    (1, "Incomplete"),
    (2, "In Progress"),
    (3, "Complete")
    )
    
    TICKET_CHOICES = (
    (1, "Request New Feature - $99.99"),
    (2, "Report Bug - Free")
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User)
    username = models.CharField(max_length=200)
    comment_num = models.IntegerField()
    upvotes = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(blank=True, null=True,
    default=timezone.now)
    ticket_type = models.IntegerField(choices=TICKET_CHOICES)

    def __str__(self):
        return self.title

class TicketType(models.Model):
    # A legend for ticket types
    
     ticket = models.ForeignKey(Ticket)
     ticket_type = models.IntegerField()
     match_ticket_id = models.IntegerField()
     ticket_title = models.CharField(max_length=200)
     value = models.DecimalField(max_digits=9, decimal_places=2)
     bug_or_request = models.CharField(max_length=7, default='bug')
    
     def __str__(self):
        return self.ticket_title
        
class Comment(models.Model):
    # The model for a comment 
    
    comment = models.TextField()
    username = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(blank=True, null=True,
    default=timezone.now)
    ticket = models.ForeignKey(Ticket)
    ticket_owner_id = models.IntegerField()

    def __str__(self):
        return self.comment 