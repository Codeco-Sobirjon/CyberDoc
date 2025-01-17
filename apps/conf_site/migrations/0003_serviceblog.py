# Generated by Django 5.1.2 on 2024-11-12 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf_site', '0002_alter_submitrequest_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Ссылка')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Блог услуги',
                'verbose_name_plural': 'Блоги услуг',
            },
        ),
    ]
