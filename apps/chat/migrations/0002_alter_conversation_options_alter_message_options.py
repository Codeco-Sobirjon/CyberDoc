# Generated by Django 5.1.3 on 2024-11-26 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversation',
            options={'verbose_name': '1. Беседа', 'verbose_name_plural': '1. Беседы'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-timestamp',), 'verbose_name': '2. Сообщение', 'verbose_name_plural': '2. Сообщения'},
        ),
    ]