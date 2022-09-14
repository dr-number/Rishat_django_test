from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from APIStripe.views import Products
from custom_user.forms import RegistrationForm, AuthorizationForm
from custom_user.models import UserCustom
from django.views.generic import TemplateView

class Registration(TemplateView):
    template_name = 'custom_user/registration.html'

    def __update_user_data(self, user):
        UserCustom.objects.update_or_create(user=user, defaults={'Description': user.custom_user.description},)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': RegistrationForm()})


    def post(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()

            raw_password = form.cleaned_data.get('password1')

            user.custom_user.description = form.cleaned_data.get('description')
            self.__update_user_data(user)  

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # redirect user to products page
            return redirect(reverse('products'))

        return render(request, self.template_name, {'form': form})

class Authorization(TemplateView):
    template_name = 'custom_user/authorisation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': AuthorizationForm()})

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            login(request,user)
            return redirect(reverse('products'))
       
        return render(request, self.template_name, {'form': AuthorizationForm(request.POST)})

def signout(request):
    logout(request)
    return redirect(reverse('products'))

