# Generated by Django 5.1.6 on 2025-03-06 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0023_alter_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.CharField(editable=False, max_length=13, primary_key=True, serialize=False, unique=True),
        ),
    ]
