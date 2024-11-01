# Generated by Django 4.2.16 on 2024-10-28 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("firmware", "0004_machine_machinelog_supportticket_delete_errorlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="machine",
            name="asset_name",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="machine",
            name="customer_name",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="machine",
            name="product_name",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
