# Generated by Django 5.0.1 on 2024-01-19 06:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_client_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.subcategory'),
        ),
    ]
