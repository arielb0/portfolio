# Generated by Django 5.0.6 on 2024-08-30 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_remove_review_title_review_email_review_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-datetime']},
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
