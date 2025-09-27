from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.core.mail import send_mail

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


class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'subject', 'created']
    readonly_fields = ['created']
    inlines = [TicketReplyInline]


    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            obj.save()
            send_mail(
                subject=f"reply to: {obj.ticket.subject}",
                message=f"(SocialMedia Admin with email: {obj.author_name.email}) said: {obj.message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[obj.ticket.author_name.email],
                fail_silently=False,
            )
            ticket = obj.ticket
            if not ticket.answered:
                ticket.answered = True
                ticket.save()
