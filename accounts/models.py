from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomUser(User):

    class Meta:
        proxy = True  
 
