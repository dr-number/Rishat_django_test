from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from custom_user.forms import SignUpForm
from custom_user.models import UserCustom

def __update_user_data(user):
    UserCustom.objects.update_or_create(user=user, defaults={'Description': user.profile.description},)

def authorization(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            user.profile.description = form.cleaned_data.get('description')
            __update_user_data(user)  

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # redirect user to products page
            return redirect('products')
    else:
        form = SignUpForm()
    return render(request, 'custom_user/signup.html', {'form': form})
