# Generated by Django 4.1.12 on 2023-11-07 17:27

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainController', '0007_alter_devices__id'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='clientes',
            field=djongo.models.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='devices',
            name='_id',
            field=models.CharField(default='d7322ec502ce4ff193775332139a8fe8', editable=False, max_length=24, primary_key=True, serialize=False),
        ),
    ]
