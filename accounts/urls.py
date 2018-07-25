from django.conf.urls import url, include
from accounts.views import user_list, register, edit_user, logout, login, profile, delete_user
from accounts import url_reset

#Patterns for accounts app functionality
urlpatterns = [
    url(r'user_list/$', user_list, name='user_list') ,
    url(r'register/', register, name='register') ,
    url(r'edit/(?P<id>\d+)$', edit_user, name='edit_user') ,
    url(r'delete/(?P<id>\d+)$', delete_user, name='delete_user') ,
    url(r'logout/$', logout, name="logout") ,
    url(r'login/$', login, name="login") ,
    url(r'profile/(?P<id>\d+)$', profile, name="profile") ,
    url(r'^password-reset/', include(url_reset)),
]
