# Generated by Django 4.2.16 on 2024-09-29 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_specialization_remove_doctor_user_delete_facility_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialization',
            name='qualification',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='specialization',
            field=models.CharField(max_length=50),
        ),
    ]