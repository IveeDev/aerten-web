# Generated by Django 5.1.6 on 2025-02-27 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0018_alter_role_employment_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='access_level',
        ),
        migrations.AddField(
            model_name='employee',
            name='access_level',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('Employee', 'Employee'), ('Guest', 'Guest')], default='Employee', max_length=100),
        ),
    ]
