from django import forms
from django.contrib.auth.models import User
from .models import Ticket, TicketType, Comment
from django.core.exceptions import ValidationError
from django.utils import timezone

class TicketForm(forms.ModelForm):
    # A form for creating a ticket
    
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'ticket_type')

class CommentForm(forms.ModelForm):
    # A form for creating a comment
    
    class Meta:
        model = Comment
        fields = ( 'comment', )
