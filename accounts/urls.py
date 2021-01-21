from django.urls import path
from accounts.views import login_view, logout_view, register_view, user_preference_view


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('user_preference/', user_preference_view, name='user_preference'),
]
