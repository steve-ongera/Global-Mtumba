from django.urls import path
from .views import signup , activate , logout_view , view_profile, update_profile
from django.contrib.auth import views as auth_views


app_name = 'accounts'


urlpatterns = [
    path('signup',signup , name='signup'),
    path('<str:username>/activate',activate),
    path('accounts/logout/', logout_view, name='logout'),

    path('profile/', view_profile, name='view_profile'),
    path('profile/update/', update_profile, name='update_profile'),
    
]
