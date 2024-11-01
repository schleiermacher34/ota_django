
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


class Customer(models.Model):
    # Assuming a simple Customer model; customize as needed
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Asset(models.Model):
    asset_no = models.CharField(max_length=36, unique=True, editable=False, default=uuid.uuid4)
    assetname = models.CharField(max_length=255)
    serialnumber = models.CharField(max_length=255, unique=True)
    datesold = models.DateField(null=True, blank=True)  # Optional
    dateinservice = models.DateField(null=True, blank=True)  # Optional
    assetstatus = models.CharField(max_length=50, null=True, blank=True)  # Optional
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)  # Optional

    # Initialize logs as an empty field (use JSONField if you need structured data in logs)
    logs = models.TextField(default="", blank=True)

    def __str__(self):
        return f"{self.assetname} - {self.asset_no}"
    def add_log(self, log_entry):
        # Method to append log entries to logs field
        current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{current_time}: {log_entry}\n"
        self.logs += log_entry
        self.save()


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


