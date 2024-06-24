# Generated by Django 4.1.13 on 2024-06-20 14:03

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupDevices',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('ipAddress', models.GenericIPAddressField()),
                ('deviceUser', models.CharField(max_length=100)),
                ('devicePassword', models.CharField(max_length=100)),
                ('controllerStatus', models.CharField(max_length=40)),
                ('deviceName', models.CharField(max_length=40)),
                ('version', models.CharField(max_length=40)),
                ('model', models.CharField(max_length=40)),
                ('vendor', models.CharField(max_length=40)),
                ('macAddress', models.CharField(max_length=40, unique=True)),
                ('clientes', djongo.models.fields.JSONField(blank=True, default=list, null=True)),
                ('status', models.IntegerField()),
                ('serialNumber', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('deviceType', models.CharField(blank=True, default='access_point', max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('interfaces', djongo.models.fields.JSONField(blank=True, default=list, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainController.groupdevices')),
            ],
        ),
    ]
