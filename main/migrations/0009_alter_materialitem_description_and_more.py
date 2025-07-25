# Generated by Django 4.2.23 on 2025-07-14 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_materialcategory_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialitem',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='materialitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='materials/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='materialitem',
            name='order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Порядок'),
        ),
    ]
