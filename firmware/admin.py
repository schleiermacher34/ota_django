from django.contrib import admin
from .models import Firmware, Machine, MachineLog, SupportTicket, DeviceUser

admin.site.register(Firmware)
admin.site.register(Machine)
admin.site.register(MachineLog)
admin.site.register(SupportTicket)
admin.site.register(DeviceUser)

