
from django.db import models

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
