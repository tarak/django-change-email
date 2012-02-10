from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from change_email.models import EmailChange
from change_email.mail import send_confirmation


def resend_confirmation(modeladmin, request, queryset):
    for object in queryset:
        send_confirmation(object)
resend_confirmation.short_description = _("Resend confirmation email to selected addresses")


class EmailChangeAdmin(admin.ModelAdmin):
    actions = [resend_confirmation]
    date_hierarchy = 'date'
    list_display = ('id', 'user', 'new_email', 'date')
    list_display_links = ('id', 'user',)
    search_fields = ('new_email', 'id', 'user__username', 'user__first_name', 'user__last_name', 'user__email',)


admin.site.register(EmailChange, EmailChangeAdmin)
