# Generated by Django 5.1.7 on 2025-03-16 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0026_employeeimage_alter_employee_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeimage',
            name='image',
            field=models.ImageField(upload_to='employee_management/images'),
        ),
    ]
