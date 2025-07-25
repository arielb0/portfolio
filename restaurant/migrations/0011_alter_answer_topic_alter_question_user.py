# Generated by Django 5.0.6 on 2024-10-09 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0010_alter_question_datetime_alter_question_prediction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='topic',
            field=models.IntegerField(choices=[(1, 'user_satisfaction'), (2, 'opening_hours'), (3, 'address'), (4, 'contact'), (5, 'menu'), (6, 'reservation'), (7, 'home_delivery'), (8, 'services'), (9, 'thanks_answer'), (10, 'positive_review'), (11, 'negative_review')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.TextField(editable=False, max_length=255, null=True),
        ),
    ]
