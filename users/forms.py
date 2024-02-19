# users/forms.py
from django import forms
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Category, UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    categories_of_interest = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False  # Make the field optional
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'categories_of_interest']

    def profile(self):
        user_profile = UserProfile.objects.get(user=self.user)
        user_categories = user_profile.categories_of_interest.all()

        return render(self, 'catalog/catalog/explore.html', {'user_categories': user_categories})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = UserProfile.objects.create(user=user)

            # Check if categories_of_interest is provided before setting
            if 'categories_of_interest' in self.cleaned_data:
                user_profile.categories_of_interest.set(self.cleaned_data['categories_of_interest'])

        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    categories_of_interest = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = User
        fields = ['username', 'email', 'categories_of_interest']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']