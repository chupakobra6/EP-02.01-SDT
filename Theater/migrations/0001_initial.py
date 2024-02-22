# Generated by Django 5.0.2 on 2024-02-20 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Имя актера')),
                ('surname', models.CharField(max_length=40, verbose_name='Фамилия актера')),
                ('patronymic', models.CharField(blank=True, max_length=40, null=True, verbose_name='Отчество актера')),
                ('role', models.CharField(max_length=255, verbose_name='Роль актера')),
            ],
            options={
                'verbose_name': 'Актёр',
                'verbose_name_plural': 'Актёры',
                'ordering': ['surname', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название зала')),
                ('number_of_rows', models.IntegerField(verbose_name='Количество рядов')),
                ('number_of_seats', models.IntegerField(verbose_name='Количество мест')),
            ],
            options={
                'verbose_name': 'Зал',
                'verbose_name_plural': 'Залы',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='PassportData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.IntegerField(verbose_name='Серия паспорта')),
                ('number', models.IntegerField(verbose_name='Номер паспорта')),
                ('place_of_issue', models.CharField(max_length=255, verbose_name='Место выдачи')),
                ('date_of_issue', models.DateField(verbose_name='Дата выдачи')),
            ],
            options={
                'verbose_name': 'Паспортные данные',
                'verbose_name_plural': 'Паспортные данные',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название должности')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ActorRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(verbose_name='Оценка')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание отзыва')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.actor', verbose_name='Актёр')),
            ],
            options={
                'verbose_name': 'Оценка актёра',
                'verbose_name_plural': 'Оценки актёров',
                'ordering': ['-grade', 'actor'],
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес картинки постера')),
                ('title', models.CharField(max_length=255, verbose_name='Название представления')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата проведения')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='Время проведения')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.hall', verbose_name='Зал')),
            ],
            options={
                'verbose_name': 'Представление',
                'verbose_name_plural': 'Представления',
                'ordering': ['date', 'time', 'title'],
            },
        ),
        migrations.CreateModel(
            name='PerformanceActor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.actor', verbose_name='Актёр')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.performance', verbose_name='Представление')),
            ],
            options={
                'verbose_name': 'Актёр представления',
                'verbose_name_plural': 'Актёры представлений',
            },
        ),
        migrations.CreateModel(
            name='PerformanceRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(verbose_name='Оценка')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание отзыва')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.performance', verbose_name='Представление')),
            ],
            options={
                'verbose_name': 'Оценка представления',
                'verbose_name_plural': 'Оценки представлений',
                'ordering': ['-grade', 'performance'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Имя')),
                ('surname', models.CharField(max_length=40, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=40, null=True, verbose_name='Отчество')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефонный номер')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Электронная почта')),
                ('login', models.CharField(max_length=255, unique=True, verbose_name='Логин')),
                ('password_hash', models.CharField(max_length=255, verbose_name='Хэш пароля')),
                ('passport_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.passportdata', verbose_name='Паспортные данные')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'ordering': ['surname', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_count', models.IntegerField(verbose_name='Номер ряда')),
                ('seat_number', models.IntegerField(verbose_name='Номер места')),
                ('status', models.BooleanField(default=True, verbose_name='Статус места')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена места')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.hall', verbose_name='Зал')),
            ],
            options={
                'verbose_name': 'Место',
                'verbose_name_plural': 'Места',
                'ordering': ['row_count', 'seat_number'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Имя клиента')),
                ('surname', models.CharField(max_length=40, verbose_name='Фамилия клиента')),
                ('patronymic', models.CharField(blank=True, max_length=40, null=True, verbose_name='Отчество клиента')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефонный номер клиента')),
                ('order_date', models.DateField(verbose_name='Дата покупки билета')),
                ('order_status', models.BooleanField(default=False, verbose_name='Статус покупки')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена билета')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.hall', verbose_name='Зал')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.performance', verbose_name='Представление')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theater.seat', verbose_name='Место')),
            ],
            options={
                'verbose_name': 'Билет',
                'verbose_name_plural': 'Билеты',
                'ordering': ['order_date', 'surname', 'name'],
            },
        ),
    ]
