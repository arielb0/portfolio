# Generated by Django 5.0.6 on 2024-08-28 16:55

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=64)),
                ('body', models.TextField(max_length=255)),
                ('prediction', models.IntegerField(blank=True, null=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=255)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.review')),
            ],
        ),
    ]
