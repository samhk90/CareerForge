# Generated by Django 5.0.3 on 2024-04-01 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='bio',
            new_name='skills',
        ),
    ]
