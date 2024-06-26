# Generated by Django 4.1.13 on 2024-06-27 00:25

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainController', '0002_devices_uplink'),
    ]

    operations = [
        migrations.CreateModel(
            name='Controllers',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('vendor', models.CharField(max_length=40)),
                ('host', models.CharField(max_length=40)),
                ('devices', djongo.models.fields.JSONField(blank=True, default=list, null=True)),
                ('clients', djongo.models.fields.JSONField(blank=True, default=list, null=True)),
                ('ipAddress', models.GenericIPAddressField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainController.groupdevices')),
            ],
        ),
    ]
