from django.urls import path
from .views import profile_view,login_view,change_password_view,logout_function

urlpatterns = [
    path('profile',profile_view,name='profile'),
    path('login',login_view,name='login'),
    path('change_password',change_password_view,name='change_password'),
    path('logout',logout_function,name='logout'),
]