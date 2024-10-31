# Generated by Django 4.0.6 on 2024-10-23 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firmware', '0002_firmware_device_type_alter_firmware_version_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=32, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('device_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firmware.deviceuser')),
            ],
        ),
    ]