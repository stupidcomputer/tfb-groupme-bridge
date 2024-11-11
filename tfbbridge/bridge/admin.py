from django.contrib import admin

from .models import Organization, Group

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    exclude = ('_sender_url', '_receiver_url')
    readonly_fields = ('add_sending_group', 'add_receiving_group', )

admin.site.register(Group)