from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import CustomUser
from .forms import UserForm, EditUserForm
from django.contrib.auth.hashers import make_password

# Create your views here.
def user_list(request):
    results = CustomUser.objects.all()
    return render(request, "user_list.html", {'tests': results})

def add_user(request):
    if request.method =="POST": 
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.password = make_password(request.POST.get('password'))
            user = CustomUser.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'), first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'))
            user.save()
            return redirect(user_list)
    else:
        form = UserForm()
 
    return render(request, "add_user.html", {'form': form})

def edit_user(request, id):
    item = get_object_or_404(CustomUser, pk=id)
    
    if request.method =="POST":
        form = EditUserForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(user_list)
    else:
        form = EditUserForm(instance=item)
    return render(request, "add_user.html", {'form': form})
    