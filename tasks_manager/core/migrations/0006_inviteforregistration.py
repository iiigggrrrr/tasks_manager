# Generated by Django 3.2.12 on 2024-06-10 01:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_companyuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteForRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invited_email', models.EmailField(max_length=254, unique=True)),
                ('prepared_role', models.CharField(choices=[('customer', 'Customer'), ('employee', 'Employee'), ('admin', 'Admin')], max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invited_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]