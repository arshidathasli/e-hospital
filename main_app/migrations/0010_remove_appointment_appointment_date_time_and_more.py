# Generated by Django 4.2.16 on 2024-10-05 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_appointment_mode_of_payment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_date_time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_date',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_time',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
