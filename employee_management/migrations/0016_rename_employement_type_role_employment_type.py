# Generated by Django 5.1.6 on 2025-02-25 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0015_rename_employement_role_employement_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='employement_type',
            new_name='employment_type',
        ),
    ]
