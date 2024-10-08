# Generated by Django 5.0.6 on 2024-08-27 16:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to='files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'pdf', 'jpg', 'jpeg', 'docx'])])),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('email_count', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
