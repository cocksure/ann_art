# Generated by Django 4.2.23 on 2025-07-15 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_projectitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectitem',
            name='category',
            field=models.CharField(choices=[('commercial', 'Коммерческие помещения'), ('residential', 'Жилые помещения'), ('other', 'Другое')], default='other', max_length=20, verbose_name='Тип проекта'),
        ),
    ]
