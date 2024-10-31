
from django.db import models
from django.contrib.auth.models import User
import uuid


class Firmware(models.Model):
    DEVICE_TYPES = (
        ('model_a', 'Model A'),
        ('model_b', 'Model B'),
        # Add your device types here
    )

    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    version = models.CharField(max_length=50)
    file = models.FileField(upload_to='firmware/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('device_type', 'version')

    def __str__(self):
        return f"Firmware {self.device_type} {self.version}"

class DeviceUser(models.Model):
    serial_number = models.CharField(max_length=32, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.serial_number


def generate_license_key():
    return uuid.uuid4().hex.upper()


class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# ota_app/models.py

from django.db import models

class Asset(models.Model):
    asset_no = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    serialnumber = models.CharField(max_length=100, unique=True)
    datesold = models.DateField(null=True, blank=True)
    dateinservice = models.DateField(null=True, blank=True)
    assetstatus = models.CharField(max_length=100)
    assetname = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    logs = models.TextField(null=True, blank=True)  # Field to store logs

    def __str__(self):
        return f"{self.assetname} ({self.serialnumber})"



class Machine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=100)
    asset_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    license_key = models.CharField(max_length=100, unique=True)
    model_name = models.CharField(max_length=100)
    activation_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.model_name} ({self.serial_number})"


class MachineLog(models.Model):
    LOG_TYPE_CHOICES = [
        ('operation', 'Operation'),
        ('error', 'Error'),
    ]

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES)
    message = models.TextField()

    def __str__(self):
        return f"{self.machine} - {self.log_type} at {self.timestamp}"

class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    issue_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')

    def __str__(self):
        return f"Ticket {self.id} - {self.status}"


