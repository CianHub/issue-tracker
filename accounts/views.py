from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import  EditUserForm, UserLogin, UserRegistrationForm
from django.contrib.auth.hashers import make_password
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from tickets.models import Ticket, TicketType, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    # Renders Home Page
    
    #Get number of new tickets added since user last logged in
    new = None
    if request.user.is_authenticated:
    
        try:
            new = request.session.get('new')
            del request.session['new']
        
        except:
            new = None
        
    return render(request, "index.html", {'new':new})
    
@staff_member_required  
def user_list(request):
    # Renders the user index page
    
    # Gets all users
    results = User.objects.all()
    
    # Pagination settings
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 10)
    
    try:
        users = paginator.page(page)
        
    except PageNotAnInteger:
        
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, "user_list.html", {'tests': results, 'users': users })

@login_required
def edit_user(request, id):
    # Renders Edit User Page
    
    # Gets the user object
    user = get_object_or_404(User, pk=id)
    
    # Prevents a user from editing another users page
    if not request.user.is_staff:
        if user.id != request.user.id:
            messages.success(request, 'You Do Not Have Permission To View This Page')
            return redirect(reverse('index'))

    # On form submission
    if request.method =="POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Changes Have Been Saved")
            return redirect(reverse('index'))
    else:
        form = EditUserForm(instance=user)
        
    return render(request, "edit_user.html", {'form': form})

@login_required
def delete_user(request, id):
    # Deletes the user
    
    # Gets the user object
    user = get_object_or_404(User, pk=id)
    
    # Prevent user deleting their own profile
    if user.id == request.user.id:
        messages.success(request, 'You cannot delete your own user profile. If you wish to remove your profile please contact a staff member.')
        return redirect(reverse('user_list'))
    
    # Delete profile
    else:
        user.delete()
        messages.success(request, 'The user has been successfully deleted.')
        return redirect(reverse('user_list'))
        
    return redirect(reverse('user_list'))
        
@login_required
def logout(request):
    # Logs the user out
    
    auth.logout(request)
    messages.success(request, 'You have successfully been logged out!')
    return redirect(reverse('index'))

def login(request):
    # Logs the user in
    
    # If the user is logged in
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    
    # If login credentials are valid
    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
         
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            
            #If user is autheticated
            if user:
                
                # Get number of tickets created since last login
                try:
                    user_login = User.objects.get(username =request.POST['username'])
                    last_login = user_login.last_login
                    new_tickets = Ticket.objects.filter(date_created__gt=last_login)
                    request.session['new'] = len(new_tickets)
                
                except:
                    user_login = User.objects.get(username =request.POST['username'])
                    last_login = user_login.last_login
                    new_tickets = Ticket.objects.filter(date_created__gt=last_login)
                    request.session['new'] = len(new_tickets)
                
                #Log in user
                auth.login(user=user, request=request)
                messages.success(request, 'You have successfully logged in!')
                return redirect(reverse('index'))
            else:
                form.add_error(None, "Your username or password is incorrect")
    else:
        form = UserLogin()
        
    return render(request, 'login.html', {"login_form": form})

def register(request):
    # Allows new users to register
    
    # If user is logged in
    if request.user.is_authenticated:
        return redirect(reverse('ticket_index'))

    # Creates the new user and logs them in
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('index'))
                
            else:
                messages.error(request, "Unable to register your account at this time")
                
    else:
        registration_form = UserRegistrationForm()
        
    return render(request, 'add_user.html', {
        "form": registration_form})
        
@login_required
def profile(request, id):
    # Displays the users profile page
    
    # Gets the user object
    user = get_object_or_404(User, pk=id)
    
    # Gets the tickets and comments created by the user
    try:
        comments = Comment.objects.filter(username=user.username).order_by('-date_updated')[:3]
    except:
        comments = "empty"
    
    try:
        tickets = Ticket.objects.filter(username=user.username).order_by('-date_updated')[:3]
    except:
        tickets = "empty"
        
    return render(request, 'profile.html', {"profile": user, 'comments':comments, 'tickets':tickets})