# Generated by Django 5.1.2 on 2024-11-01 10:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firmware', '0007_asset_logs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportticket',
            name='machine',
        ),
        migrations.RemoveField(
            model_name='machinelog',
            name='machine',
        ),
        migrations.RemoveField(
            model_name='supportticket',
            name='user',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='product',
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asset',
            name='asset_no',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='assetstatus',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='firmware.customer'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='logs',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='asset',
            name='serialnumber',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='Machine',
        ),
        migrations.DeleteModel(
            name='MachineLog',
        ),
        migrations.DeleteModel(
            name='SupportTicket',
        ),
    ]
