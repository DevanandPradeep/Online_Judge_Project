# Generated by Django 4.2.23 on 2025-07-07 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='problems_solved',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='total_score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
