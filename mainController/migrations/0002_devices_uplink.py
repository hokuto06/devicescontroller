# Generated by Django 4.1.13 on 2024-06-20 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainController', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='uplink',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
