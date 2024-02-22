from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.urls import reverse


class Position(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название должности')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['title']

    def __str__(self):
        return self.title


class PassportData(models.Model):
    series_validator = RegexValidator(
        regex=r'^\d{4}$',
        message="Серия паспорта должна состоять из 4 цифр."
    )
    number_validator = RegexValidator(
        regex=r'^\d{6}$',
        message="Номер паспорта должен состоять из 6 цифр."
    )
    place_of_issue_validator = MinLengthValidator(
        limit_value=3,
        message="Место выдачи должно содержать минимум 3 символа."
    )

    series = models.CharField(
        max_length=4,
        validators=[series_validator],
        verbose_name='Серия паспорта'
    )
    number = models.CharField(
        max_length=6,
        validators=[number_validator],
        verbose_name='Номер паспорта'
    )
    place_of_issue = models.CharField(
        max_length=255,
        validators=[place_of_issue_validator],
        verbose_name='Место выдачи'
    )
    date_of_issue = models.DateField(verbose_name='Дата выдачи')

    class Meta:
        verbose_name = 'Паспортные данные'
        verbose_name_plural = 'Паспортные данные'

    def __str__(self):
        return f"{self.series} {self.number}"


class Employee(models.Model):
    name = models.CharField(max_length=40, verbose_name='Имя', validators=[MinLengthValidator(2)])
    surname = models.CharField(max_length=40, verbose_name='Фамилия', validators=[MinLengthValidator(2)])
    patronymic = models.CharField(max_length=40, verbose_name='Отчество', null=True, blank=True)
    phone_number = models.CharField(max_length=15, verbose_name='Телефонный номер', null=True, blank=True, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$',
                       message="Номер телефона должен быть введен в формате: '+999999999'. До 15 цифр.")])
    email = models.EmailField(verbose_name='Электронная почта', null=True, blank=True)
    login = models.CharField(max_length=255, verbose_name='Логин', unique=True, validators=[MinLengthValidator(5)])
    password_hash = models.CharField(max_length=255, verbose_name='Хэш пароля')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность')
    passport_data = models.ForeignKey(PassportData, on_delete=models.CASCADE, verbose_name='Паспортные данные')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['surname', 'name']

    def __str__(self):
        return f"{self.surname} {self.name}"

    def get_update_url(self):
        return reverse('employee_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('employee_delete', kwargs={'pk': self.pk})


class Hall(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название зала')
    number_of_rows = models.IntegerField(verbose_name='Количество рядов')
    number_of_seats = models.IntegerField(verbose_name='Количество мест')

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Seat(models.Model):
    row_count = models.IntegerField(verbose_name='Номер ряда')
    seat_number = models.IntegerField(verbose_name='Номер места')
    status = models.BooleanField(default=True, verbose_name='Статус места')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена места')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name='Зал')

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ['row_count', 'seat_number']

    def __str__(self):
        return f"Ряд {self.row_count}, Место {self.seat_number}"


class Actor(models.Model):
    name = models.CharField(max_length=40, verbose_name='Имя актера')
    surname = models.CharField(max_length=40, verbose_name='Фамилия актера')
    patronymic = models.CharField(max_length=40, verbose_name='Отчество актера', null=True, blank=True)
    role = models.CharField(max_length=255, verbose_name='Роль актера')

    class Meta:
        verbose_name = 'Актёр'
        verbose_name_plural = 'Актёры'
        ordering = ['surname', 'name']

    def __str__(self):
        return f"{self.surname} {self.name} - {self.role}"


class Performance(models.Model):
    poster = models.CharField(max_length=255, verbose_name='Адрес картинки постера', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название представления')
    date = models.DateField(verbose_name='Дата проведения', null=True, blank=True)
    time = models.TimeField(verbose_name='Время проведения', null=True, blank=True)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name='Зал')

    class Meta:
        verbose_name = 'Представление'
        verbose_name_plural = 'Представления'
        ordering = ['date', 'time', 'title']

    def __str__(self):
        return self.title


class Ticket(models.Model):
    name = models.CharField(max_length=40, verbose_name='Имя клиента')
    surname = models.CharField(max_length=40, verbose_name='Фамилия клиента')
    patronymic = models.CharField(max_length=40, verbose_name='Отчество клиента', null=True, blank=True)
    phone_number = models.CharField(max_length=15, verbose_name='Телефонный номер клиента', null=True, blank=True)
    order_date = models.DateField(verbose_name='Дата покупки билета')
    order_status = models.BooleanField(default=False, verbose_name='Статус покупки')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена билета')
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, verbose_name='Представление')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name='Зал')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name='Место')

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        ordering = ['order_date', 'surname', 'name']

    def __str__(self):
        return f"{self.surname} {self.name} - {self.performance.title}"


class PerformanceActor(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, verbose_name='Представление')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, verbose_name='Актёр')

    class Meta:
        verbose_name = 'Актёр представления'
        verbose_name_plural = 'Актёры представлений'

    def __str__(self):
        return f"{self.performance.title} - {self.actor}"


class ActorRating(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, verbose_name='Актёр')
    grade = models.IntegerField(verbose_name='Оценка')
    description = models.CharField(max_length=255, verbose_name='Описание отзыва', null=True, blank=True)

    class Meta:
        verbose_name = 'Оценка актёра'
        verbose_name_plural = 'Оценки актёров'
        ordering = ['-grade', 'actor']

    def __str__(self):
        return f"{self.actor} - Оценка: {self.grade}"


class PerformanceRating(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, verbose_name='Представление')
    grade = models.IntegerField(verbose_name='Оценка')
    description = models.CharField(max_length=255, verbose_name='Описание отзыва', null=True, blank=True)

    class Meta:
        verbose_name = 'Оценка представления'
        verbose_name_plural = 'Оценки представлений'
        ordering = ['-grade', 'performance']

    def __str__(self):
        return f"{self.performance} - Оценка: {self.grade}"
