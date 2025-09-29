from django.contrib.admin.models import LogEntry

def user_activities(user, limit=10):
    return LogEntry.objects.filter(user=user)[:limit]