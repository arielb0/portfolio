# Generated by Django 5.1.4 on 2024-12-15 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bazaar', '0011_alter_ad_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['priority'], 'verbose_name_plural': 'categories'},
        ),
    ]
