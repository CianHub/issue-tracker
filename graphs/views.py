from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.contrib.auth.hashers import make_password
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.utils import timezone
from tickets.models import Ticket, TicketType, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from graphs.models import Ticket_Time
import os
from datetime import timedelta, datetime

@login_required
def charts(request):
    # Loads charts
    
    # List for storing chart data
    chart_data = []
    chart_data2 = []
    
    # Get the top 3 most upvoted feature request tickets 
    highest_voted = Ticket.objects.filter(
        ticket_type=1).order_by('-upvotes')[:3]
    
    """Add the get the title and number of 
    upvotes of the top 3 most upvoted feature request tickets""" 
    for x in highest_voted:
        chart_data.append([x.title, x.upvotes])
        
    """ Get the ids of the top 3 most upvoted feature 
    request tickets and exclude them from the query"""
    excluded_ids = []
    for i in highest_voted:
        excluded_ids.append(i.id)
    
    other = Ticket.objects.filter(ticket_type=1).exclude(
        id__in=excluded_ids).order_by('-upvotes')
    
    # Get the total upvotes of the rest of the feature request tickets
    other_tickets = 0
    for upvotes in other:
        other_tickets = upvotes.upvotes + other_tickets 
    
    chart_data.append(['Other', other_tickets])
    
    # Get the top 3 most upvoted bug report tickets 
    highest_voted_bugs = Ticket.objects.filter(
        ticket_type=2).order_by('-upvotes')[:3]
    
    """ Add the get the title and number 
    of upvotes of the top 3 most upvoted bug report tickets"""
    for x in highest_voted_bugs:
        chart_data2.append([x.title, x.upvotes])
        
    """ Get the ids of the top 3 most upvoted bug report tickets 
    and exclude them from the query"""
    excluded_ids_bugs = []
    for i in highest_voted_bugs:
        excluded_ids_bugs.append(i.id)
    
    other_bugs = Ticket.objects.filter(ticket_type=2).exclude(
        id__in=excluded_ids_bugs).order_by('-upvotes')
    
    # Get the total upvotes of the rest of the bug report tickets
    other_tickets_bugs = 0
    for upvotes in other_bugs:
        other_tickets_bugs = upvotes.upvotes + other_tickets_bugs 
    
    chart_data2.append(['Other', other_tickets_bugs])
    
    # Get all completed ticket times
    times = Ticket_Time.objects.filter(date_completed__isnull=False)
    
    # Store completion numbers
    completed_daily = 0
    completed_weekly = 0
    completed_monthly = 0
    
    
    #Check how many tickets were completed within the respective time
    for i in times:
        diff = i.date_completed - i.date_started
        days = diff.days

        if days < 1:
            completed_daily+=1
            completed_weekly+=1
            completed_monthly+=1
        elif days < 7:
            completed_weekly+=1
            completed_monthly+=1
        elif days < 30:
            completed_monthly+=1
            
    return render(request, 'charts.html', {'chart_data':chart_data, 'chart_data2': chart_data2,'completed_daily': str(completed_daily), 'completed_weekly': str(completed_weekly), 'completed_monthly': str(completed_monthly)})