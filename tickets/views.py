from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import TicketForm, CommentForm, TicketTypeForm
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


@login_required
def ticket_index(request):
    # Display an index of existing tickets
    
    user = request.user
    ticket_list = Ticket.objects.filter(date_updated__lte=timezone.now()).order_by('-date_updated')
    
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
    # Display the details a post
    
    ticket = get_object_or_404(Ticket, pk=id)
    
    ticket_type = TicketType.objects.get(match_ticket_id=id)
    
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
        form = CommentForm()
    
    return render(request, 'ticket_detail.html', { 'ticket': ticket, 'comments': comments, 'form':form, 'type':ticket_type})

@login_required()
def create_ticket(request, pk=None):
    # Allows the user to create a new bug report ticket
    
    instance = Ticket(author=request.user, username=request.user.username, status=1, comment_num=0, upvotes=0)
    
    if request.method == 'POST':
        
        form = TicketForm(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            ticket = form.save(commit=False)
            
            if ticket.ticket_type == 2:
                
                ticket.save()
    
                ticket_type = TicketType(ticket=ticket, ticket_type=ticket.ticket_type, match_ticket_id=ticket.id, ticket_title=ticket.title, bug_or_request='bug', value=0)
                
                ticket_type.save()
                
                return redirect(view_ticket, ticket.pk)
                
            else:
                
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

    stripe.api_key = settings.STRIPE_SECRET
    
    ticket_val = request.session.get('ticket_val')
    
    if request.method == 'POST':
        token = request.POST['stripeToken'] 
    
        try:
            customer = stripe.Charge.create(
                amount=9999,
                currency='usd',
                description='New Feature Request',
                source=token,
                )
                
        except stripe.error.CardError:
                messages.error(request, "Your card was declined")
                
        if customer.paid:
                ticket = Ticket(author=request.user, username=request.user.username, status=1, comment_num=0, upvotes=0, ticket_type=1, description=ticket_val['description'], title=ticket_val['title'])
            
                ticket.save()
                
                ticket_type = TicketType(ticket=ticket, ticket_type=ticket.ticket_type, match_ticket_id=ticket.id, ticket_title=ticket.title, bug_or_request='feature', value=99.99)
                ticket_type.save()
                
                messages.success(request, "Your Payment Was Successful. Your Feature Request Ticket Has Been Created.")
                return redirect(view_ticket, ticket.pk)

        else:
            messages.error(request, "Unable to take payment.")
                
    return render(request, 'ticket_payment.html')

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

    return redirect(view_ticket, ticket.pk)
    
def upvote_ticket_request(request, id):
    # Upvotes the ticket if its a request and is paid for
    
    stripe.api_key = settings.STRIPE_SECRET
    
    ticket = get_object_or_404(Ticket, pk=id)
    
    if request.method == 'POST':
        token = request.POST['stripeToken'] 
    
        try:
            customer = stripe.Charge.create(
                amount=999,
                currency='usd',
                description='New feature request - upvote',
                source=token,
                )
                
        except stripe.error.CardError:
                messages.error(request, "Your card was declined")
                
        if customer.paid:
            
            ticket.upvotes += 1
            ticket.save()

            messages.success(request, "Your Payment Was Successful. Your upvote has been registered.")
            return redirect(view_ticket, ticket.pk)

        else:
            messages.error(request, "Unable to take payment.")
                
    return render(request, 'ticket_payment.html')

