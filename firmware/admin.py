from django.contrib import admin
from .models import Firmware, Machine, MachineLog, SupportTicket, DeviceUser, Customer, Asset

admin.site.register(Firmware)
admin.site.register(MachineLog)
admin.site.register(SupportTicket)
admin.site.register(Customer)
admin.site.register(Asset)

