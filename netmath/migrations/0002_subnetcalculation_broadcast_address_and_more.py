# Generated by Django 5.2.1 on 2025-06-25 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netmath', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subnetcalculation',
            name='broadcast_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subnetcalculation',
            name='first_host',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subnetcalculation',
            name='last_host',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subnetcalculation',
            name='network_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
