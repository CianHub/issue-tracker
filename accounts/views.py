from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .models import CustomUser
from .forms import UserForm, EditUserForm, UserLogin, UserRegistrationForm
from django.contrib.auth.hashers import make_password
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    #renders index.html
    return render(request, "index.html")
    
@login_required   
def user_list(request):
    results = CustomUser.objects.all()
    return render(request, "user_list.html", {'tests': results})

"""def add_user(request):
    if request.method =="POST": 
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.password = make_password(request.POST.get('password'))
            user = CustomUser.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'), first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'))
            user.save()
            return redirect(index)
    else:
        form = UserForm()
 
    return render(request, "add_user.html", {'form': form})"""

@login_required
def edit_user(request, id):
    user = get_object_or_404(User, pk=id)
    
    if request.method =="POST":
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(user_list)
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, "add_user.html", {'form': form})

@login_required
def logout(request):
    # Logs user out
    auth.logout(request)
    messages.success(request, 'You have successfully been logged out!')
    return redirect(reverse('index'))

def login(request):
    # Return a login page
    if request.user.is_authenticated:
        return redirect(reverse('index'))
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
    # Render the registration page
    if request.user.is_authenticated:
        return redirect(reverse('index'))

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
    # The users profile page
    user = User.objects.get(id=request.user.id)
    # Add query to pull and display a users comments and tickets here
    return render(request, 'profile.html', {"profile": user})
    