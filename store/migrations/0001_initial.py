# Generated by Django 5.1.5 on 2025-01-20 02:04

import store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Category Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Category Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', validators=[store.models.validate_image_size], verbose_name='Category Image')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
    ]
