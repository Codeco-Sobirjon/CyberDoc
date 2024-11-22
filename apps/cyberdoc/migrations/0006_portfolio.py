# Generated by Django 5.1.2 on 2024-11-22 14:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyberdoc', '0005_orderwork_foreign_sources'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Название портфолио')),
                ('file', models.FileField(blank=True, null=True, upload_to='portfolio/', verbose_name='Файл')),
                ('views', models.IntegerField(blank=True, default=0, null=True, verbose_name='Зрители')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Дата публикации')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_portfolio', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь портфолио',
                'verbose_name_plural': 'Пользователь портфолио',
            },
        ),
    ]
