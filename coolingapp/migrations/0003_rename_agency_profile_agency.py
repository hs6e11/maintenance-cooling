# Generated by Django 4.2.5 on 2023-09-15 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coolingapp', '0002_remove_profile_address_profile_agency_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Agency',
            new_name='agency',
        ),
    ]