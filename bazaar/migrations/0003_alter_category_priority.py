# Generated by Django 5.0.6 on 2024-08-19 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazaar', '0002_alter_category_parent_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='priority',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
