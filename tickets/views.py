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
import stripe
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os

@login_required
def ticket_index(request):
    # Display an index of existing tickets
    
    # Get logged in user
    user = request.user
    
    # Get all tickets in order of latest -> oldest
    ticket_list = Ticket.objects.filter(date_updated__lte=timezone.now()).order_by('-date_updated')
    
    # Pagination settings
    page = request.GET.get('page', 1)
    paginator = Paginator(ticket_list, 10)
    
    try:
        tickets = paginator.page(page)
        
    except PageNotAnInteger:
        
        tickets = paginator.page(1)
        
    except EmptyPage:
        
        tickets = paginator.page(paginator.num_pages)

    return render(request, "ticket_index.html", {'tickets': tickets, 'user':user})
    
@login_required
def view_ticket(request, id):
    # Display the tickets information and enable users to upvote or comment on the ticket
    
    # Gets the selected ticket and companion tickettype object
    ticket = get_object_or_404(Ticket, pk=id)
    ticket_type = TicketType.objects.get(match_ticket_id=id)
    
    # Gets the comments associated with the ticket and displays them newest -> oldest
    try:
        comments = Comment.objects.filter(ticket=ticket).order_by('-date_updated')
    except:
        comments = "empty"
        
    # Adds the logged in users username and ticket information automatically before a comment is created
    instance = Comment(username=request.user.username, ticket=ticket, ticket_owner_id=ticket.id)
    
    # When user posts a comment the ticket is updated
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            ticket.comment_num = (len(comments) +1 )
            ticket.save()
            form.save()
            return redirect(view_ticket, ticket.pk)
    else:
        form = CommentForm()
    
    return render(request, 'ticket_detail.html', { 'ticket': ticket, 'comments': comments, 'form':form, 'type':ticket_type})

@login_required()
def create_ticket(request, pk=None):
    # Allows the user to create a new ticket
    
    # The ticket is automatically associated with the logged in user
    instance = Ticket(author=request.user, username=request.user.username, status=1, comment_num=0, upvotes=0)
    
    # When the create ticket form is submitted it is handled based on it's ticket type
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            ticket = form.save(commit=False)
            
            # If ticket is a bug report
            if ticket.ticket_type == 2:
                
                ticket.save()
                ticket_type = TicketType(ticket=ticket, ticket_type=ticket.ticket_type, match_ticket_id=ticket.id, ticket_title=ticket.title, bug_or_request='bug', value=0)
                ticket_type.save()
                
                return redirect(view_ticket, ticket.pk)
                
            # If ticket is a request for a new feature  
            else:
                
                # Submitted info is stored in the session 
                ticket_val = {
                    'title': request.POST['title'],
                    'description': request.POST['description']
                }
                
                request.session['ticket_val'] = ticket_val

                return redirect(pay_for_ticket)
    else:
        form = TicketForm()
    
    return render(request, 'create_ticket.html', {'form': form})

@login_required
def pay_for_ticket(request):
    # Enables the user to make the payment necessary for creating a request feature ticket
    
    value = 9999
    description = 'New Feature Request'
    
    # Gets Stripe secret key
    stripe.api_key = settings.STRIPE_SECRET
    
    # Gets the submitted values from the create ticket view
    ticket_val = request.session.get('ticket_val')
        
    if ticket_val == None:
        messages.success(request, 'You Do Not Have Permission To View This Page')
        return redirect(reverse('index'))
            
    # Processes the users payment via Stripe
    if request.method == 'POST':
        token = request.POST['stripeToken'] 
    
        try:
                customer = stripe.Charge.create(
                amount=value,
                currency='usd',
                description='New Feature Request',
                source=token,
                )
                
        except stripe.error.CardError:
                messages.error(request, "Your card was declined")
                
        # If the payment is successful the ticket and associated ticketype are created
        if customer.paid:
                ticket = Ticket(
                        author=request.user, username=request.user.username, status=1, comment_num=0,
                        upvotes=0, ticket_type=1, description=ticket_val['description'], title=ticket_val['title']
                        )
                ticket.save()
                
                ticket_type = TicketType(ticket=ticket, ticket_type=ticket.ticket_type, match_ticket_id=ticket.id, ticket_title=ticket.title, bug_or_request='feature', value=99.99)
                ticket_type.save()
                
                messages.success(request, "Your Payment Was Successful. Your Feature Request Ticket Has Been Created.")
                del request.session['ticket_val']
                return redirect(view_ticket, ticket.pk)
        else:
            messages.error(request, "Unable to take payment.")
                
    return render(request, 'ticket_payment.html', {'value':value, 'description': description})

@login_required
def edit_ticket(request, id):
    # Allows the user to edit a ticket
    
    # Gets the current ticket
    ticket = get_object_or_404(Ticket, pk=id)
    
    # Only the user who created the ticket may edit it    
    if ticket.username != request.user.username:
        messages.success(request, 'You Do Not Have Permission To View This Page')
        return redirect(reverse('index'))
        
    if request.method == 'POST':
        
        # Fills the edit form with information from the ticket
        form = TicketForm(request.POST, instance=ticket)
        
        # Upon submission the tickets date_updated is updated
        if form.is_valid():
            ticket.date_updated = datetime.datetime.now()
            form.save()
            
            messages.success(request, "Your Changes Have Been Saved")
            return redirect(view_ticket, ticket.id)
    
    else:
        form = TicketForm(instance=ticket)
            
    return render(request, 'edit_ticket.html', {'form': form})

@login_required
def delete_ticket(request, id):
    # Allows the user to delete the ticket
    
    # Gets the current tickety
    ticket = get_object_or_404(Ticket, pk=id)
    
    # Only a ticket with a status of incomplete may be deleted
    if ticket.status == 1:
        ticket.delete()
        return redirect(reverse('index'))
    elif ticket.status == 2:
        messages.success(request, 'This ticket cannot be deleted as it is already in progress.')
        return redirect(reverse('index'))
    else:
        messages.success(request, 'This ticket cannot be deleted as it is already complete.')
        return redirect(reverse('index'))
        
@login_required
def upvote_ticket(request, id):
    # Upvotes the ticket
    
    # Gets current object and increments upvotes by 1
    ticket = get_object_or_404(Ticket, pk=id)
    ticket.upvotes += 1
    ticket.save()

    return redirect(view_ticket, ticket.pk)
 
@login_required   
def upvote_ticket_request(request, id):
    # Enables the user to make the payment for upvoting a feature request ticket
    
    # Gets the Stripe secret key
    stripe.api_key = settings.STRIPE_SECRET
    
    value = 999
    description = 'Upvote New Feature Request'
    
    ticket = get_object_or_404(Ticket, pk=id)
    
    if int(ticket.id) != int(id):
        print(ticket.id)
        print(id)
        messages.success(request, 'You Do Not Have Permission To View This Page')
        return redirect(reverse('index'))
    
    else:
        # Processes the users payment via Stripe    
        if request.method == 'POST':
            
            token = request.POST['stripeToken'] 
    
            try:
                customer = stripe.Charge.create(
                amount=value,
                currency='usd',
                description='Upvote New Feature Request',
                source=token,
                )
                
            except stripe.error.CardError:
                messages.error(request, "Your card was declined")
                
            # If the payment is successful the ticket is updated
            if customer.paid:
            
                ticket.upvotes += 1
                ticket.save()

                messages.success(request, "Your Payment Was Successful. Your upvote has been registered.")
                return redirect(view_ticket, ticket.pk)

            else:
                messages.error(request, "Unable to take payment.")
        
    return render(request, 'ticket_payment.html', {'value':value, 'description': description})

