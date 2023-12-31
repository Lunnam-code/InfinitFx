from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import User
from django.utils.html import format_html


class UserAdmin(UserAdmin):
    list_display = ('id','email','first_name','last_name','username','account_balance', 'last_login','date_joined','is_active')
    list_display_links = ('email','first_name','last_name','username')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    
    
admin.site.register(User, UserAdmin)