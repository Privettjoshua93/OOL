# Generated by Django 5.1 on 2024-09-05 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_onboardingfield_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onboarding',
            name='field',
        ),
        migrations.RemoveField(
            model_name='onboarding',
            name='value',
        ),
        migrations.AddField(
            model_name='onboarding',
            name='field_data',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='onboarding',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
