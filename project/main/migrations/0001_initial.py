# Generated by Django 5.1 on 2024-09-01 05:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Offboarding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('last_date_time', models.DateTimeField()),
                ('additional_notes', models.TextField()),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('details', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Onboarding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('preferred_work_email', models.EmailField(max_length=100)),
                ('personal_email', models.EmailField(max_length=100)),
                ('mobile_number', models.CharField(max_length=15)),
                ('title', models.CharField(max_length=100)),
                ('manager', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('mac_or_pc', models.CharField(choices=[('Mac', 'Mac'), ('PC', 'PC')], max_length=3)),
                ('start_date', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('groups', models.TextField()),
                ('distribution_lists', models.TextField()),
                ('shared_drives', models.TextField()),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('details', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='LOA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
