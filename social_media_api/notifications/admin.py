from django.contrib import admin
from .models import Notification

# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'actor', 'verb', 'read', 'timestamp')
    list_filter = ('verb', 'read', 'timestamp')
    search_fields = ('recipient__username', 'actor__username')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('Base Information', {
            'fields': ('recipient', 'actor', 'verb', 'read')
        }),
        ('Target Object', {
            'fields': ('target_content_type', 'target_object_id')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
