"""issuetracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url 
from django.contrib import admin
from accounts.views import  user_list, add_user, edit_user

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', user_list) ,
    url(r'add_user$', add_user) ,
    url(r'^edit/(?P<id>\d+)$', edit_user) , 
    
    #(?P<id>\d+) = ?P<id> means its an expression called id, \d+ means the expression is a digit the + means it can be more than 1 digit
    
    
    #calling the view function, $ signifies the end of the url, basically everything between the last r'^ and ' is what goes at the end of the url e.g. blank is index/homepage as there is nothing added e.g. if theres no ^ as long as the url ends with the text before the $ it will work
    
]
