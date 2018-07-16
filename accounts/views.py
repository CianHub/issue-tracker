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
    
    return render(request, "index.html")
    
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
    
    # Gets the current user
    user = get_object_or_404(User, pk=id)
    
    # Prevents a user from editing another users oage
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
            if user:
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
        return redirect(reverse('index'))

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
def profile(request):
    # Displays the users profile page
    
    # Gets the logged in user
    user = User.objects.get(id=request.user.id)
    
    # Gets the tickets and comments created by the logged in user
    try:
        comments = Comment.objects.filter(username=request.user.username).order_by('-date_updated')[:3]
    except:
        comments = "empty"
    
    try:
        tickets = Ticket.objects.filter(username=request.user.username).order_by('-date_updated')[:3]
    except:
        comments = "empty"
        
    return render(request, 'profile.html', {"profile": user, 'comments':comments, 'tickets':tickets})