from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from change_email.models import EmailChange


def resend_confirmation(modeladmin, request, queryset):
    """
An admin action function to resend confirmation mails to
pending change request addresses.
"""
    for object in queryset:
        object.send_confirmation_mail()
resend_confirmation.short_description = _("Resend confirmation email"
                                          " to selected addresses")


class EmailChangeAdmin(admin.ModelAdmin):
    """
A ModelAdmin class to represent an :model:`EmailChange` model in the
admin interface.
"""
    actions = [resend_confirmation]
    date_hierarchy = 'date'
    list_display = ('id', 'user', 'new_email', 'date')
    list_display_links = ('id', 'user',)
    list_editable = ('new_email',)
    search_fields = ('new_email', 'id', 'user__id', 'user__username',
                     'user__first_name', 'user__last_name', 'user__email',)

    def get_readonly_fields(self, request, obj=None):
        """
Sets the ``user`` and the ``date`` field to read only if an instance
already exists.
"""
        if obj:
            return ['user']
        else:
            return []


admin.site.register(EmailChange, EmailChangeAdmin)
