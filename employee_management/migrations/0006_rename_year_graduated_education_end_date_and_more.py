# Generated by Django 5.1.4 on 2025-01-16 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0005_alter_permission_options_alter_role_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='education',
            old_name='year_graduated',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='education',
            old_name='year_admitted',
            new_name='start_date',
        ),
    ]
