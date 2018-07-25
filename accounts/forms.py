from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class EditUserForm(forms.ModelForm):
    # Form For Editing User Details
    
    def clean_email(self):
        # Prevent Duplicate Emails and Usernames
        
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address must be unique')
            
        return email
        
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'is_staff')
        
    def __init__(self, *args, **kwargs):
        # Make Fields Required
        
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class UserLogin(forms.Form):
    # Form For Logging in Users
    
    username = forms.CharField(label="Username or Email Address")
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    # Form To Register New Users
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_email(self):
        # Prevent Duplicate Emails and Usernames
        
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address must be unique')
        return email

    def clean_password2(self):
        # Ensure Passwords Match
        
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Please confirm your password")
        
        if password1 != password2:
            raise ValidationError("Passwords must match")
        
        return password2
        
    def __init__(self, *args, **kwargs):
        # Make Fields Required
        
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True