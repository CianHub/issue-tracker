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
from graphs.models import Ticket_Time
import os

@login_required
def ticket_index(request):
    # Display an index of existing tickets
    
    # Get logged in user
    user = request.user
    
    # Get all tickets in order of latest -> oldest
    ticket_list = Ticket.objects.filter(
        date_updated__lte=timezone.now()).order_by('-date_updated'
        )
    
    # Pagination settings
    page = request.GET.get('page', 1)
    paginator = Paginator(ticket_list, 10)
    
    try:
        tickets = paginator.page(page)
        
    except PageNotAnInteger:
        
        tickets = paginator.page(1)
        
    except EmptyPage:
        
        tickets = paginator.page(paginator.num_pages)

    return render(
        request, "ticket_index.html", {'tickets': tickets, 'user':user}
        )
    
@login_required
def view_ticket(request, id):
    # Display the tickets information and enable users to add upvotes or comments 
    
    # Gets the selected ticket and companion tickettype object
    ticket = get_object_or_404(Ticket, pk=id)
    ticket_type = TicketType.objects.get(match_ticket_id=id)
    
    # Gets comments associated with ticket and displays them newest -> oldest
    try:
        comments = Comment.objects.filter(
            ticket=ticket).order_by('-date_updated'
            )
    except:
        comments = "empty"
        
    # New comment set up
    instance = Comment(
        username=request.user.username,
        ticket=ticket,
        ticket_owner_id=request.user.id
        )
    
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
    
    return render(
        request,
        'ticket_detail.html', {
            'ticket': ticket,
            'comments': comments,
            'form':form, 'type':ticket_type
            }
        )

@login_required()
def create_ticket(request, pk=None):
    # Allows the user to create a new ticket
    
    # New Ticket set up
    instance = Ticket(
        author=request.user,
        username=request.user.username,
        status=1,
        comment_num=0,
        upvotes=0
        )
    
    # Form is handled based on it's ticket type
    if request.method == 'POST':
        form = TicketForm(
            request.POST, request.FILES, instance=instance
            )
        
        if form.is_valid():
            ticket = form.save(commit=False)
            
            # If ticket is a bug report
            if ticket.ticket_type == 2:
                
                ticket.save()
                ticket_type = TicketType(
                    ticket=ticket,
                    ticket_type=ticket.ticket_type,
                    match_ticket_id=ticket.id,
                    ticket_title=ticket.title,
                    bug_or_request='bug',
                    value=0
                    )
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
    # Enables the user to pay for a request feature ticket
    
    # Info for web page
    purchase = 'create a new feature request ticket'
    value = 9999
    description = 'New Feature Request'
    price = str(round((value / 100), 2))
    
    # Gets Stripe secret key
    stripe.api_key = settings.STRIPE_SECRET
    
    # Gets the submitted values from the create ticket view
    ticket_val = request.session.get('ticket_val')
        
    # If user hasn't submitted a feature request ticket
    if ticket_val == None:
        messages.success(
            request, 'You Do Not Have Permission To View This Page'
            )
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
                
        # If the payment is successful
        if customer.paid:
                ticket = Ticket(
                        author=request.user,
                        username=request.user.username,
                        status=1,
                        comment_num=0,
                        upvotes=0,
                        ticket_type=1,
                        description=ticket_val['description'],
                        title=ticket_val['title']
                        )
                ticket.save()
                
                ticket_type = TicketType(
                    ticket=ticket,
                    ticket_type=ticket.ticket_type,
                    match_ticket_id=ticket.id,
                    ticket_title=ticket.title,
                    bug_or_request='feature',
                    value=99.99
                    )
                ticket_type.save()
                
                messages.success(
                    request,
                    "Your Payment Was Successful. Your Feature Request Ticket Has Been Created."
                    )
                del request.session['ticket_val']
                return redirect(view_ticket, ticket.pk)
        else:
            messages.error(request, "Unable to take payment.")
                
    return render(
        request,
        'ticket_payment.html', {
            'value':value,
            'description': description,
            'purchase':purchase,
            'price': price
            
        })

@login_required
def edit_ticket(request, id):
    # Allows the user to edit a ticket
    
    # Gets the current ticket
    ticket = get_object_or_404(Ticket, pk=id)
    current_status = ticket.status
    
    if request.method == 'POST':
        
        # Fills the edit form with information from the ticket
        form = TicketForm(request.POST, instance=ticket)
        
        # Upon submission the tickets date_updated is updated
        if form.is_valid():
            
            # If ticket status is incomplete
            if form.cleaned_data['status'] == 1:
                
                try: 
                    time = Ticket_Time.objects.get(match_ticket_id=id)
                    time.date_started = None
                    time.date_completed = None
                    time.date_difference = None
                    
                except:
                    time = Ticket_Time(
                        ticket=ticket,
                        match_ticket_id=ticket.id
                        )
                
                ticket.date_updated = datetime.datetime.now()
                ticket.save()
                form.save()
                time.save()
                
                messages.success(request, "Your Changes Have Been Saved")
                return redirect(view_ticket, ticket.id)
                
            # If ticket status changes from incomplete to in progress
            if current_status == 1 and form.cleaned_data['status'] == 2:
                
                try: 
                    time = Ticket_Time.objects.get(match_ticket_id=id)
                    time.date_started = datetime.datetime.now()
                    time.date_completed = None
                    time.date_difference = None
                    
                except:
                    time = Ticket_Time(
                        ticket=ticket,
                        match_ticket_id=ticket.id,
                        date_started=datetime.datetime.now()
                        )
                
                ticket.date_updated = datetime.datetime.now()
                ticket.save()
                form.save()
                time.save()
                
                messages.success(request, "Your Changes Have Been Saved")
                return redirect(view_ticket, ticket.id)
                
            # If ticket status changes from in progress to complete
            elif current_status == 2 and form.cleaned_data['status'] == 3:
                time = Ticket_Time.objects.get(match_ticket_id=id)
                
                time.date_completed = datetime.datetime.now()
                
                ticket.date_updated = datetime.datetime.now()
                
                time.save()
                form.save()
                ticket.save()

                messages.success(request, "Your Changes Have Been Saved")
                return redirect(view_ticket, ticket.id)
                
            else:
                ticket.date_updated = datetime.datetime.now()
                 
                form.save()
                ticket.save()
                
                messages.success(request, "Your Changes Have Been Saved")
                return redirect(view_ticket, ticket.id)
                
    else:
        form = TicketForm(instance=ticket)
            
    return render(request, 'edit_ticket.html', {'form': form})

@login_required
def delete_ticket(request, id):
    # Allows the user to delete the ticket
    
    # Gets the ticket object
    ticket = get_object_or_404(Ticket, pk=id)
    
    # Only a ticket with a status of incomplete may be deleted
    if ticket.status == 1:
        ticket.delete()
        return redirect(reverse('ticket_index'))
        
    elif ticket.status == 2:
        messages.success(
            request,
            'This ticket cannot be deleted as it is already in progress.'
            )
        return redirect(reverse('ticket_index'))
        
    else:
        messages.success(
            request,
            'This ticket cannot be deleted as it is already complete.'
            )
        return redirect(reverse('ticket_index'))
        
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
    # Enables the user to pay for upvoting a feature request ticket
    
    # Gets the Stripe secret key
    stripe.api_key = settings.STRIPE_SECRET
    
    # Page info
    value = 999
    description = 'Upvote New Feature Request'
    purchase = 'upvote a new feature request ticket.'
    price = str(round((value / 100), 2))
    
    #Get ticket info and make sure ticket is correct
    ticket = get_object_or_404(Ticket, pk=id)
    
    if int(ticket.id) != int(id):
      
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
                
            # If the payment is successful 
            if customer.paid:
            
                ticket.upvotes += 1
                ticket.save()

                messages.success(
                    request,
                    "Your Payment Was Successful. Your upvote has been registered."
                    )
                return redirect(view_ticket, ticket.pk)

            else:
                messages.error(request, "Unable to take payment.")
        
    return render(
        request,
        'ticket_payment.html', {
            'value':value,
            'description': description,
            'purchase':purchase,
            'price': price
            
        })

@login_required
def delete_comment(request, id):
    # Deletes comment
    
    # Gets the relevent objects
    comment = get_object_or_404(Comment, pk=id)
    ticket = get_object_or_404(Ticket, pk=comment.ticket.id)
    comments = Comment.objects.filter(ticket=ticket)
    
    # Deletes the comment
    ticket.comment_num = (len(comments ) -1 )
    ticket.save()
    comment.delete()
    
    messages.success(request, 'The comment was successfully deleted.')
    return redirect(view_ticket, ticket.pk)

@login_required
def edit_comment(request, id):
    # Edit comment page
    
    # Gets the relevent objects
    comment = get_object_or_404(Comment, pk=id)
    ticket = get_object_or_404(Ticket, pk=comment.ticket.id)
    comments = Comment.objects.filter(ticket=ticket)
    user = request.user
    
    # Prevents a non-staff user from editing another users comment
    if not request.user.is_staff:
        if user.id != request.user.id:
            messages.success(
                request,
                'You Do Not Have Permission To View This Page'
                )
            return redirect(view_ticket, ticket.pk)

    # On form submission
    if request.method =="POST":
        
        form = CommentForm(request.POST, instance=comment)
        
        if form.is_valid():
            form.save()
            comment.date_updated = datetime.datetime.now()
            comment.save()
            ticket.save()

            messages.success(
                request,
                'The comment was successfully edited.'
                )
            return redirect(view_ticket, ticket.pk)
    else:
        form = CommentForm(instance=comment)
        
    return render(request, 'edit_comment.html',{'form': form})