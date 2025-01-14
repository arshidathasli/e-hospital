# Generated by Django 4.2.16 on 2024-10-07 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_medication_prescription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medication',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='medication',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='patient',
        ),
        migrations.AddField(
            model_name='medication',
            name='appointment',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main_app.appointment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prescription',
            name='appointment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.appointment'),
            preserve_default=False,
        ),
    ]
