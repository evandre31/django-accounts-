from django.shortcuts import render, redirect
from .models import Profile
from .forms import SignupForm, UserForm, ProfileForm
from django.contrib.auth import authenticate, login


def signup(request):
    if request.method == 'POST':  # save
        form = SignupForm(request.POST)
        if form.is_valid():  # si valide  alors save
            form.save()  # save mais sans login
            mon_username = form.cleaned_data['username']  # extraire username depuis le form
            mon_password = form.cleaned_data['password1']  # extraire password depuis le form
            user = authenticate(username=mon_username, password=mon_password)  # préparer le user
            login(request, user)  # faire le login
            return redirect('/accounts/profile')  # redirect vers ...
    else:  # show form
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request):
    profile_ = Profile.objects.get(user=request.user)  # get profile qui a user(dans profile) = au user request
    return render(request, 'profile/profile.html', {'profile': profile_})


def profile_edit(request):
    profile_ = Profile.objects.get(user=request.user)  # get profile qui a user(dans profile) = au user request
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=request.user)
        profileform = ProfileForm(request.POST, instance=profile_)
        if userform.is_valid() and profileform.is_valid():
            userform.save()  # save user directement mais le profile nécessité la suivante
            myform = profileform.save(commit=False)  # s'assurer que le profile est relié au user
            myform.user = request.user  # s'assurer que le profile est relié au user
            myform.save()  # save profile
            return redirect('accounts:profile')
    else:   # (affichage)
        userform = UserForm(instance=request.user)    # request.user = data du user connecté (affichage)
        profileform = ProfileForm(instance=profile_)  # profile_ = profile du user connecté  (affichage)
    return render(request, 'profile/profile_edit.html', {'userform': userform, 'profileform': profileform})

