# Generated by Django 5.0.3 on 2024-04-01 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0002_rename_bio_profile_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cover_letter',
            field=models.TextField(blank=True),
        ),
    ]
