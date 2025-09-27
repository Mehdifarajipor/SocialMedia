from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Social.models import *


# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'phone_number', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {'fields': ('phone_number', 'bio', 'job', 'photo', 'date_of_birth')}),
    )
    inlines = (CommentInline,)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created']
    date_hierarchy = 'created'
    inlines = [CommentInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'subject']
