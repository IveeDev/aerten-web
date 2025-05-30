# Generated by Django 5.1.6 on 2025-02-16 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0007_alter_education_course_of_study_alter_employee_team_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
