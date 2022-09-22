from django.utils import timezone
from main.functions import get_client_ip
from custom_user.models import TemporaryBanIp


class BanIP():

    request = None
    obj = None

    small_attempts = 0
    long_attempts = 0


    def __init__(self, small_attempts: int, long_attempts: int):
        self.request = None
        self.small_attempts = small_attempts
        self.long_attempts = long_attempts

    def check(self, request):
        self.request = request

        ip = get_client_ip(request)
       
        self.obj, created = TemporaryBanIp.objects.get_or_create(
            defaults={
                'ip_address': ip,
                'time_unblock': timezone.now()
            },
            ip_address=ip
        )
 
        # if the IP is blocked and it's not time to unblock
        if self.obj.status is True and self.obj.time_unblock > timezone.now():
            if self.obj.attempts == self.small_attempts:
                return 'banSmall'
            elif self.obj.attempts >= self.long_attempts:
                return 'banLong'
        
        # if the IP is blocked, but it's time to unblock, then unblock the IP
        if self.obj.status is True and self.obj.time_unblock < timezone.now():
            self.obj.status = False
            self.obj.save()

        return ''

    def delete_record(self):
        self.obj.delete()

    def increment_ban_count(self):
        if self.obj.attempts  <= self.long_attempts:
            self.obj.attempts += 1

        if self.obj.attempts == self.small_attempts:
            self.obj.time_unblock = timezone.now() + timezone.timedelta(minutes=self.small_attempts)
            self.obj.status = True
        elif self.obj.attempts == self.long_attempts:
            self.obj.time_unblock = timezone.now() + timezone.timedelta(minutes=self.long_attempts)
            self.obj.status = True

        self.obj.save()