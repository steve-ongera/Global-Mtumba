from django.shortcuts import render , redirect
from .forms import *
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.views import View

from django.conf import settings


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            # Create user object but don't save it yet
            user = form.save(commit=False)
            user.is_active = False  # Initially, set the user as inactive
            user.save()
            
            # Create or update the profile associated with this user
            profile = Profile.objects.get(user__username=username)
            
            # Send activation email
            send_mail(
                "Activate Your Account",
                f"Welcome {username} \nuse this code {profile.code} to activate your account",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
                
            return redirect(f'/accounts/{username}/activate')
            
    else:
        form = SignupForm()
    
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def activate(request, username):
    # Fetch profile of the user
    profile = Profile.objects.get(user__username=username)

    if request.method == 'POST':
        form = ActivationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']

            # Check if the entered code matches the code stored in the profile
            if code == profile.code:
                # Clear the activation code after successful activation
                profile.code = ''

                # Activate the user account
                user = User.objects.get(username=profile.user.username)
                user.is_active = True  # Correct the field name to 'is_active'
                user.save()

                # Save the profile
                profile.save()

                # Redirect to login page
                return redirect('/accounts/login')
            else:
                # If the code doesn't match, you could add an error message
                form.add_error('code', 'Invalid activation code.')
    else:
        form = ActivationForm()

    return render(request, 'registration/activate.html', {'form': form})



def view_profile(request):
    # Get the profile of the logged-in user
    profile = Profile.objects.get(user=request.user)
    
    return render(request, 'registration/view_profile.html', {'profile': profile})


def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    user = request.user  # Get the User object

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            # Update user fields (first_name, last_name, email)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Save the updated profile
            form.save()
            return redirect('accounts:view_profile')  # Redirect to the profile page or any other page
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'registration/update_profile.html', {'form': form})