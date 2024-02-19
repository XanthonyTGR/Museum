from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    try:
        profile_instance = request.user.profile
    except ObjectDoesNotExist:
        # If the profile doesn't exist, create a new one
        Profile.objects.create(user=request.user)
        # Retrieve the newly created profile
        profile_instance = request.user.profile

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)


def login_redirect(request):
    user = request.user

    if user.is_authenticated:
        if hasattr(user, 'profile') and user.profile.is_museum:
            # Redirect to the inventory page for museums
            return redirect('inventory')
        else:
            # Redirect to the profile page for normal users
            return redirect('profile')
    else:
        # Handle the case where the user is not authenticated
        # You might want to redirect them to the login page or display an error message
        return redirect('login')
