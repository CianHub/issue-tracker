from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'last_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'last_name', 'email')