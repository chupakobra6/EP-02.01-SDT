from django import forms

from Theater.models import PerformanceRating, ActorRating, Ticket, Employee, PassportData, PerformanceActor, Position, \
    Hall, Seat, Actor, Performance


class PerformanceRatingForm(forms.ModelForm):
    class Meta:
        model = PerformanceRating
        fields = ['grade', 'description', 'performance']


class ActorRatingForm(forms.ModelForm):
    class Meta:
        model = ActorRating
        fields = ['grade', 'description', 'actor']


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=64)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'surname', 'patronymic', 'phone_number', 'order_date', 'order_status', 'price', 'performance',
                  'hall', 'seat']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'order_status': forms.CheckboxInput(),
            'performance': forms.Select(),
            'hall': forms.Select(),
            'seat': forms.Select(),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'minlength': '2'}),
            'surname': forms.TextInput(attrs={'minlength': '2'}),
            'login': forms.TextInput(attrs={'minlength': '5'}),
        }


class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ['poster', 'title', 'date', 'time', 'hall']


class PerformanceActorForm(forms.ModelForm):
    class Meta:
        model = PerformanceActor
        fields = ['performance', 'actor']


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'surname', 'patronymic', 'role']


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ['title', 'number_of_rows', 'number_of_seats']


class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ['row_count', 'seat_number', 'status', 'price', 'hall']


class PassportDataForm(forms.ModelForm):
    class Meta:
        model = PassportData
        fields = '__all__'
        widgets = {
            'series': forms.NumberInput(attrs={'min': '1000', 'max': '9999'}),
            'number': forms.NumberInput(attrs={'min': '100000', 'max': '999999'}),
            'place_of_issue': forms.TextInput(attrs={'minlength': '3'}),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title']
