# Generated by Django 4.1.12 on 2023-10-24 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainController', '0007_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='_id',
            field=models.CharField(default='aea64269c1104d1797407cdeca7d2fb0', editable=False, max_length=24, primary_key=True, serialize=False),
        ),
    ]