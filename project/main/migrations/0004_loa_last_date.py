# Generated by Django 5.1 on 2024-09-05 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_azurecredentials_smtp_host_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loa',
            name='last_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
