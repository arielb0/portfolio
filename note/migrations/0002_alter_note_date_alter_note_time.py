# Generated by Django 5.1.3 on 2024-11-20 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='note',
            name='time',
            field=models.TimeField(auto_now=True, verbose_name='Time'),
        ),
    ]
