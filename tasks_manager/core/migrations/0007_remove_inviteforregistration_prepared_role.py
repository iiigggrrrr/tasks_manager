# Generated by Django 3.2.12 on 2024-06-10 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_inviteforregistration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inviteforregistration',
            name='prepared_role',
        ),
    ]
