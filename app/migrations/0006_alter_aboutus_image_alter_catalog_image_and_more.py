# Generated by Django 5.0.1 on 2024-01-22 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_client_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutus',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='AboutUs/'),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='Catalog/'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='Product/'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='image_type',
            field=models.CharField(choices=[('product', 'Product'), ('partner', 'Partner'), ('mobile', 'Mobile'), ('main', 'Main')], default='product', max_length=8),
        ),
    ]