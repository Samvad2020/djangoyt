from django.urls import path
from .views import signup, login, logout, post_signup

urlpatterns = [
    path('signup', signup, name="signup"),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('postsignup/', post_signup, name='postsignup')

]

