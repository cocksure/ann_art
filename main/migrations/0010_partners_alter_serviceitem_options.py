# Generated by Django 4.2.23 on 2025-07-14 07:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_materialitem_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('order', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Порядок отображения')),
                ('image', models.ImageField(blank=True, default='default_foto.png', upload_to='partners/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'heic'])], verbose_name='Фото партнеры')),
            ],
            options={
                'verbose_name': 'Партнер',
                'verbose_name_plural': 'Партнеры',
                'ordering': ('order',),
            },
        ),
        migrations.AlterModelOptions(
            name='serviceitem',
            options={'ordering': ('order',), 'verbose_name': 'Услуга', 'verbose_name_plural': 'Услуги'},
        ),
    ]
