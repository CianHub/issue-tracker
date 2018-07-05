from django.conf.urls import url, include
from accounts.views import user_list, register, edit_user, logout, login, profile
from accounts import url_reset

urlpatterns = [
    url(r'user_list/$', user_list, name='user_list') ,
    url(r'register/', register, name='register') ,
    url(r'edit/(?P<id>\d+)', edit_user, name='edit_user') ,
    url(r'logout/', logout, name="logout") ,
    url(r'login/', login, name="login") ,
    url(r'profile/$', profile, name="profile") ,
    url(r'^password-reset/', include(url_reset))

]
