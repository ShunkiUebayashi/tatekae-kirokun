from django.contrib import admin

from .models import ApprovedInvoice, CustomUser, PendingInvoice

admin.site.register(PendingInvoice)
admin.site.register(ApprovedInvoice)
admin.site.register(CustomUser)
