from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from custom_user.forms import RegistrationForm, AuthorizationForm
from django.views.generic import TemplateView

from django.views import View
from main.constants import BAN_IP_LONG_ATTEMPTS, BAN_IP_LONG_TIME_MINUTES, BAN_IP_SMALL_ATTEMPTS, BAN_IP_SMALL_TIME_MINUTES
from main.functions import custom_render
from main.security import BanIP
from custom_user.models import UserCustom

class Registration(TemplateView):
    template_name = 'custom_user/registration.html'

    def __update_user_data(self, user):
        UserCustom.objects.update_or_create(user=user, defaults={'Description': user.custom_user.description},)
    
    def get(self, request, *args, **kwargs):
        return custom_render(request, self.template_name, {'form': RegistrationForm()})


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

        return custom_render(request, self.template_name, {'form': form})

class Authorization(TemplateView):
    template_name = 'custom_user/authorisation.html'
    banIP = BanIP(BAN_IP_SMALL_ATTEMPTS, BAN_IP_LONG_ATTEMPTS)

    def get(self, request, *args, **kwargs):
        return custom_render(request, self.template_name, {'form': AuthorizationForm()})

    def post(self, request, *args, **kwargs):

        redirect_ban_ip = self.banIP.check(request)

        if redirect_ban_ip:
            return redirect(reverse(redirect_ban_ip))

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)
 
        if user is not None:
            self.banIP.delete_record()
            login(request, user)
            return redirect(reverse('products'))
        else:
            self.banIP.increment_ban_count()
       
        return custom_render(request, self.template_name, {'form': AuthorizationForm(request.POST)})

class Signout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('products'))

class BanIpPage(View):
    template_name = 'main/ban_ip.html'

    def get(self, request, *args, **kwargs):

        if request.GET.get('time') == 'banSmall':
            time = BAN_IP_SMALL_TIME_MINUTES
        else:
            time = BAN_IP_LONG_TIME_MINUTES

        return custom_render(request, self.template_name, {
            'title': 'Ban IP',
            'time' : time
        })