from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Social.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'phone_number', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {'fields': ('phone_number', 'bio', 'job', 'photo', 'date_of_birth')}),
    )