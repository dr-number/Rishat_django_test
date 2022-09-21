from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import TemporaryBanIp, UserCustom

class UserInline(admin.StackedInline):
    model = UserCustom
    can_delete = False
    verbose_name_plural = 'Sub info'

class TemporaryBanIpAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'status', 'attempts', 'time_unblock')
    search_fields = ('ip_address',)
 
class UserAdmin(UserAdmin):
    inlines = (UserInline, )
 
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(TemporaryBanIp, TemporaryBanIpAdmin)