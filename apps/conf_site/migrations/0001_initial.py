# Generated by Django 5.1.2 on 2024-11-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='Заголовок')),
                ('image', models.ImageField(blank=True, null=True, upload_to='service/', verbose_name='Изображение')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуга',
            },
        ),
        migrations.CreateModel(
            name='SubmitRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Полное имя')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('topic', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тема работы')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Срок сдачи')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Отправить заявку',
                'verbose_name_plural': 'Отправить заявку',
            },
        ),
    ]
