from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import TicketForm, CommentForm
from django.contrib.auth.hashers import make_password
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Ticket, TicketType, Comment
import datetime

@login_required
def ticket_index(request):
    # Display an index of existing tickets
    
    user = request.user
    tickets = Ticket.objects.filter(date_updated__lte=timezone.now()).order_by('-date_updated')

    
    
    return render(request, "ticket_index.html", {'tickets': tickets, 'user':user})
    
@login_required
def view_ticket(request, id):
    # Display the details a post
    
    ticket = get_object_or_404(Ticket, pk=id)
    
    try:
        comments = Comment.objects.filter(ticket=ticket).order_by('-date_updated')
    except:
        comments = "empty"

    instance = Comment(username=request.user.username, ticket=ticket, ticket_owner_id=ticket.id)
    
    if request.method == 'POST':
        
        if 'upvote' in request.POST:
            print('upvote')
        
        else:
            form = CommentForm(request.POST, request.FILES, instance=instance)
        
            if form.is_valid():
                ticket.comment_num = (len(comments) +1 )
                ticket.save()
                form.save()
            
                return redirect(view_ticket, ticket.pk)
        
            
    else:
        form = CommentForm(request.POST, request.FILES)
    
    return render(request, 'ticket_detail.html', { 'ticket': ticket, 'comments': comments, 'form':form})

@login_required
def create_ticket_type(request, pk=None):
    # Allows the user to select the type of ticket

    return render(request, 'create_ticket.html')

@login_required()
def create_ticket_bug(request, pk=None):
    # Allows the user to create a new bug report ticket
    
    instance = Ticket(author=request.user, username=request.user.username, ticket_type=2, status=1, comment_num=0, upvotes=0)
    
    if request.method == 'POST':
        
        form = TicketForm(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            ticket = form.save()
            
            ticket_type = TicketType(ticket=ticket, ticket_type=ticket.ticket_type, match_ticket_id=ticket.id, ticket_title=ticket.title, bug_or_request='bug')
            ticket_type_saved = ticket_type.save()
            
            return redirect(view_ticket, ticket.pk)
            
    
    else:
        form = TicketForm(request.POST, request.FILES)
    
    return render(request, 'create_ticket_bug_form.html', {'form': form})

@login_required()
def create_ticket_feature(request, pk=None):
    # Allows the user to create a new bug report ticket
    
    instance = Ticket(author=request.user, username=request.user.username, ticket_type=2, status=1, comment_num=0, upvotes=0)
    
    if request.method == 'POST':
        
        form = TicketForm(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            ticket = form.save()
            
            ticket_type = TicketType(ticket=ticket, ticket_type=ticket.ticket_type, match_ticket_id=ticket.id, ticket_title=ticket.title, value= None, bug_or_request='bug')
            ticket_type_saved = ticket_type.save()
            
            return redirect(view_ticket, ticket.pk)
        
    else:
        form = TicketForm(request.POST, request.FILES)
    
    return render(request, 'create_ticket_bug_form.html', {'form': form})

@login_required
def edit_ticket(request, id):
    # Allows the user to edit a ticket
    
    ticket = get_object_or_404(Ticket, pk=id)

    if ticket.username != request.user.username:
        messages.success(request, 'You Do Not Have Permission To View This Page')
        return redirect(reverse('index'))
        
    if request.method == 'POST':
        
        form = TicketForm(request.POST, instance=ticket)
        
        if form.is_valid():
            ticket.date_updated = datetime.datetime.now()
            form.save()
            
            messages.success(request, "Your Changes Have Been Saved")
            return redirect(view_ticket, ticket.id)
    
    else:
        form = TicketForm(instance=ticket)
            
    return render(request, 'edit_ticket.html', {'form': form})

@login_required
def upvote_ticket(request, id):
    # Upvotes the ticket
    
    ticket = get_object_or_404(Ticket, pk=id)
    ticket.upvotes += 1
    ticket.save()
    print(ticket.upvotes)
            
    return redirect(view_ticket, ticket.pk)
    
    



