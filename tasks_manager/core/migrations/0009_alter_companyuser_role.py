# Generated by Django 3.2.12 on 2024-06-11 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyuser',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('employee', 'Employee'), ('advanced_employee', 'Advanced Employee'), ('admin', 'Admin')], max_length=64),
        ),
    ]
