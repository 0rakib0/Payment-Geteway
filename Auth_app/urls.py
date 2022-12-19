from django.urls import path
from Auth_app import views


app_name = 'Auth_App'

urlpatterns = [
    path('signup/', views.Sing_up, name='sign_up'),
    path('login/', views.Login_user, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.User_profile, name='profile'),
    
]
