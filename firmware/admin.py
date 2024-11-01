from django.contrib import admin
from .models import Firmware, Customer, Asset

admin.site.register(Firmware)
admin.site.register(Customer)
admin.site.register(Asset)

