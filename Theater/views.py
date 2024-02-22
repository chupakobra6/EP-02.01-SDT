import hashlib
import io

import xlsxwriter
from django.contrib import messages
from django.db.models import Avg, Count, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .decorators import position_required
from .forms import ActorRatingForm, LoginForm, TicketForm, EmployeeForm, PositionForm, \
    PerformanceRatingForm, HallForm, SeatForm, ActorForm, PerformanceForm, PassportDataForm, PerformanceActorForm
from .models import Performance, Actor, Employee, Seat, Ticket, Hall, Position, PerformanceRating, ActorRating, \
    PassportData, PerformanceActor


# Create your views here.
def home(request):
    upcoming_performances = Performance.objects.all().order_by('date', 'time')[:5]
    return render(request, 'profile/home.html', {'performances': upcoming_performances})


def all_performances(request):
    performances = Performance.objects.all().order_by('title')
    return render(request, 'profile/performances.html', {'performances': performances})


def review_page(request):
    performances = Performance.objects.all()
    actors = Actor.objects.all()
    if request.method == 'POST':
        if 'performance_review' in request.POST:
            p_form = PerformanceRatingForm(request.POST)
            if p_form.is_valid():
                p_form.save()
                return redirect('review_page')
        elif 'actor_review' in request.POST:
            a_form = ActorRatingForm(request.POST)
            if a_form.is_valid():
                a_form.save()
                return redirect('review_page')
    else:
        p_form = PerformanceRatingForm()
        a_form = ActorRatingForm()
    return render(request, 'profile/reviews.html', {
        'performances': performances,
        'actors': actors,
        'p_form': p_form,
        'a_form': a_form
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_hash = hashlib.sha256((login + password).encode('utf-8')).hexdigest()

            try:
                employee = Employee.objects.get(login=login, password_hash=password_hash)
                request.session['employee_id'] = employee.id
                request.session['employee_position'] = employee.position.title
                request.session['is_authenticated'] = True
                messages.success(request, "Авторизация успешна")
                return redirect('profile')
            except Employee.DoesNotExist:
                messages.error(request, "Неверный логин или пароль")
    else:
        form = LoginForm()
    return render(request, 'profile/login.html', {'form': form})


@position_required(['Директор', 'Кассир', 'Администратор'])
def logout_view(request):
    request.session.flush()
    return redirect('home')


@position_required(['Директор', 'Кассир', 'Администратор'])
def profile_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    employee_id = request.session.get('employee_id')
    employee = Employee.objects.get(id=employee_id)

    return render(request, 'profile/profile.html', {'employee': employee})


@position_required(['Кассир', 'Администратор'])
def create_ticket(request):
    today_date = timezone.now().date()
    today_tickets = Ticket.objects.filter(order_date=today_date).order_by('order_date')
    performances = Performance.objects.all()
    seats = Seat.objects.none()

    if request.method == 'POST':
        if 'change_status' in request.POST:
            ticket_id = request.POST.get('ticket_id')
            ticket = get_object_or_404(Ticket, id=ticket_id)
            ticket.order_status = not ticket.order_status
            ticket.save()
            return redirect('create_ticket')
        else:
            form = TicketForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('create_ticket')
    else:
        form = TicketForm()

    context = {
        'today_tickets': today_tickets,
        'form': form,
        'performances': performances,
        'seats': seats,
    }
    return render(request, 'profile/create_ticket.html', context)


@position_required(['Кассир', 'Администратор'])
@csrf_exempt
def seats_view(request):
    performances = Performance.objects.all()
    selected_performance_id = request.POST.get('performance_id')
    selected_performance = None
    rows = {}

    if selected_performance_id:
        selected_performance = get_object_or_404(Performance, pk=selected_performance_id)
    elif performances:
        selected_performance = performances.first()

    if selected_performance:
        seats = Seat.objects.filter(hall=selected_performance.hall).order_by('row_count', 'seat_number')
        for seat in seats:
            rows.setdefault(seat.row_count, []).append(seat)

    if request.method == 'POST' and 'seat_id' in request.POST:
        seat_id = request.POST.get('seat_id')
        seat = get_object_or_404(Seat, pk=seat_id)
        seat.status = not seat.status
        seat.save()
        return redirect(request.path)

    context = {
        'performances': performances,
        'selected_performance': selected_performance,
        'rows': rows,
    }
    return render(request, 'profile/seats.html', context)


@position_required(['Директор', 'Администратор'])
def employees_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employees_list.html', {'employees': employees})


@position_required(['Директор', 'Администратор'])
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employees_list')


@position_required(['Директор', 'Администратор'])
def halls_list(request):
    halls = Hall.objects.all()
    return render(request, 'halls/halls_list.html', {'halls': halls})


@position_required(['Директор', 'Администратор'])
def hall_create(request):
    if request.method == "POST":
        form = HallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('halls_list')
    else:
        form = HallForm()
    return render(request, 'halls/hall_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def hall_edit(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    if request.method == "POST":
        form = HallForm(request.POST, instance=hall)
        if form.is_valid():
            form.save()
            return redirect('halls_list')
    else:
        form = HallForm(instance=hall)
    return render(request, 'halls/hall_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def hall_delete(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    hall.delete()
    return redirect('halls_list')


@position_required(['Директор', 'Администратор'])
def seats_list(request):
    seats = Seat.objects.all()
    return render(request, 'seats/seats_list.html', {'seats': seats})


@position_required(['Директор', 'Администратор'])
def seat_create(request):
    if request.method == "POST":
        form = SeatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seats_list')
    else:
        form = SeatForm()
    return render(request, 'seats/seat_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def seat_edit(request, pk):
    seat = get_object_or_404(Seat, pk=pk)
    if request.method == "POST":
        form = SeatForm(request.POST, instance=seat)
        if form.is_valid():
            form.save()
            return redirect('seats_list')
    else:
        form = SeatForm(instance=seat)
    return render(request, 'seats/seat_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def seat_delete(request, pk):
    seat = get_object_or_404(Seat, pk=pk)
    seat.delete()
    return redirect('seats_list')


@position_required(['Директор', 'Администратор'])
def actors_list(request):
    actors = Actor.objects.all()
    return render(request, 'actors/actors_list.html', {'actors': actors})


@position_required(['Директор', 'Администратор'])
def actor_create(request):
    if request.method == "POST":
        form = ActorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('actors_list')
    else:
        form = ActorForm()
    return render(request, 'actors/actor_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def actor_edit(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    if request.method == "POST":
        form = ActorForm(request.POST, instance=actor)
        if form.is_valid():
            form.save()
            return redirect('actors_list')
    else:
        form = ActorForm(instance=actor)
    return render(request, 'actors/actor_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def actor_delete(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    actor.delete()
    return redirect('actors_list')


@position_required(['Директор', 'Администратор'])
def performances_list(request):
    performances = Performance.objects.all()
    return render(request, 'performances/performances_list.html', {'performances': performances})


@position_required(['Директор', 'Администратор'])
def performance_create(request):
    if request.method == "POST":
        form = PerformanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performances_list')
    else:
        form = PerformanceForm()
    return render(request, 'performances/performance_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def performance_edit(request, pk):
    performance = get_object_or_404(Performance, pk=pk)
    if request.method == "POST":
        form = PerformanceForm(request.POST, instance=performance)
        if form.is_valid():
            form.save()
            return redirect('performances_list')
    else:
        form = PerformanceForm(instance=performance)
    return render(request, 'performances/performance_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def performance_delete(request, pk):
    performance = get_object_or_404(Performance, pk=pk)
    performance.delete()
    return redirect('performances_list')


@position_required(['Директор', 'Администратор'])
def passport_data_list(request):
    passport_data = PassportData.objects.all()
    return render(request, 'passport_data/passport_data_list.html', {'passport_data': passport_data})


@position_required(['Директор', 'Администратор'])
def passport_data_create(request):
    if request.method == "POST":
        form = PassportDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('passport_data_list')
    else:
        form = PassportDataForm()
    return render(request, 'passport_data/passport_data_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def passport_data_edit(request, pk):
    passport_data = get_object_or_404(PassportData, pk=pk)
    if request.method == "POST":
        form = PassportDataForm(request.POST, instance=passport_data)
        if form.is_valid():
            form.save()
            return redirect('passport_data_list')
    else:
        form = PassportDataForm(instance=passport_data)
    return render(request, 'passport_data/passport_data_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def passport_data_delete(request, pk):
    passport_data = get_object_or_404(PassportData, pk=pk)
    passport_data.delete()
    return redirect('passport_data_list')


@position_required(['Директор', 'Администратор'])
def performance_actor_list(request):
    performance_actors = PerformanceActor.objects.all()
    return render(request, 'performance_actors/performance_actor_list.html', {'performance_actors': performance_actors})


@position_required(['Директор', 'Администратор'])
def performance_actor_create(request):
    if request.method == "POST":
        form = PerformanceActorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance_actor_list')
    else:
        form = PerformanceActorForm()
    return render(request, 'performance_actors/performance_actor_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def performance_actor_edit(request, pk):
    performance_actor = get_object_or_404(PerformanceActor, pk=pk)
    if request.method == "POST":
        form = PerformanceActorForm(request.POST, instance=performance_actor)
        if form.is_valid():
            form.save()
            return redirect('performance_actor_list')
    else:
        form = PerformanceActorForm(instance=performance_actor)
    return render(request, 'performance_actors/performance_actor_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def performance_actor_delete(request, pk):
    performance_actor = get_object_or_404(PerformanceActor, pk=pk)
    performance_actor.delete()
    return redirect('performance_actor_list')


@position_required(['Директор', 'Администратор'])
def actor_rating_list(request):
    actor_ratings = ActorRating.objects.all()
    return render(request, 'actor_ratings/actor_rating_list.html', {'actor_ratings': actor_ratings})


@position_required(['Директор', 'Администратор'])
def actor_rating_create(request):
    if request.method == "POST":
        form = ActorRatingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('actor_rating_list')
    else:
        form = ActorRatingForm()
    return render(request, 'actor_ratings/actor_rating_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def actor_rating_edit(request, pk):
    actor_rating = get_object_or_404(ActorRating, pk=pk)
    if request.method == "POST":
        form = ActorRatingForm(request.POST, instance=actor_rating)
        if form.is_valid():
            form.save()
            return redirect('actor_rating_list')
    else:
        form = ActorRatingForm(instance=actor_rating)
    return render(request, 'actor_ratings/actor_rating_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def actor_rating_delete(request, pk):
    actor_rating = get_object_or_404(ActorRating, pk=pk)
    actor_rating.delete()
    return redirect('actor_rating_list')


@position_required(['Директор', 'Администратор'])
def performance_rating_list(request):
    performance_ratings = PerformanceRating.objects.all()
    return render(request, 'performance_ratings/performance_rating_list.html',
                  {'performance_ratings': performance_ratings})


@position_required(['Директор', 'Администратор'])
def performance_rating_create(request):
    if request.method == "POST":
        form = PerformanceRatingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance_rating_list')
    else:
        form = PerformanceRatingForm()
    return render(request, 'performance_ratings/performance_rating_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def performance_rating_edit(request, pk):
    performance_rating = get_object_or_404(PerformanceRating, pk=pk)
    if request.method == "POST":
        form = PerformanceRatingForm(request.POST, instance=performance_rating)
        if form.is_valid():
            form.save()
            return redirect('performance_rating_list')
    else:
        form = PerformanceRatingForm(instance=performance_rating)
    return render(request, 'performance_ratings/performance_rating_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def performance_rating_delete(request, pk):
    performance_rating = get_object_or_404(PerformanceRating, pk=pk)
    performance_rating.delete()
    return redirect('performance_rating_list')


@position_required(['Директор', 'Администратор'])
def positions_list(request):
    positions = Position.objects.all()
    return render(request, 'positions/positions_list.html', {'positions': positions})


@position_required(['Директор', 'Администратор'])
def position_create(request):
    if request.method == "POST":
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('positions_list')
    else:
        form = PositionForm()
    return render(request, 'positions/position_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def position_edit(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == "POST":
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            return redirect('positions_list')
    else:
        form = PositionForm(instance=position)
    return render(request, 'positions/position_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    position.delete()
    return redirect('positions_list')


@position_required(['Директор', 'Администратор'])
def tickets_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/tickets_list.html', {'tickets': tickets})


@position_required(['Директор', 'Администратор'])
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tickets_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def ticket_edit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('tickets_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'tickets/ticket_form.html', {'form': form})


@position_required(['Директор', 'Администратор'])
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.delete()
    return redirect('tickets_list')


@position_required(['Директор', 'Администратор'])
def export_tickets_report(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Отчет о продажах билетов')

    columns = ['Дата представления', 'Название представления', 'Проданные билеты', 'Общий доход', 'Средняя цена билета']
    worksheet.write_row('A1', columns)

    # Агрегация данных по каждому представлению
    aggregated_tickets = Ticket.objects.filter(order_status=True).values(
        'performance__title',
        'performance__date'
    ).annotate(
        sold_tickets=Count('id'),
        total_income=Sum('price'),
        average_price=Avg('price')
    ).order_by('performance__date')

    row = 1
    for ticket in aggregated_tickets:
        performance_date = ticket['performance__date'].strftime('%Y-%m-%d') if ticket['performance__date'] else 'N/A'
        data_row = [
            performance_date,
            ticket['performance__title'],
            ticket['sold_tickets'],
            ticket['total_income'],
            ticket['average_price']
        ]
        worksheet.write_row(row, 0, data_row)
        row += 1

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="tickets_report.xlsx"'
    return response


@position_required(['Директор', 'Администратор'])
def export_performance_ratings_report(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Оценки представлений')

    columns = ['Название представления', 'Средняя оценка', 'Количество оценок']
    worksheet.write_row('A1', columns)

    performances = PerformanceRating.objects.values('performance__title').annotate(average_rating=Avg('grade'),
                                                                                   count=Count('id')).order_by(
        'performance__title')
    row = 1
    for performance in performances:
        worksheet.write(row, 0, performance['performance__title'])
        worksheet.write(row, 1, performance['average_rating'])
        worksheet.write(row, 2, performance['count'])
        row += 1

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="performance_ratings_report.xlsx"'
    return response


@position_required(['Директор', 'Администратор'])
def export_actor_ratings_report(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Оценки актёров')

    columns = ['Фамилия и имя актёра', 'Средняя оценка', 'Количество оценок']
    worksheet.write_row('A1', columns)

    actors = ActorRating.objects.values('actor__surname', 'actor__name').annotate(average_rating=Avg('grade'),
                                                                                  count=Count('id')).order_by(
        '-average_rating')
    row = 1
    for actor in actors:
        actor_full_name = f"{actor['actor__surname']} {actor['actor__name']}"
        worksheet.write(row, 0, actor_full_name)
        worksheet.write(row, 1, actor['average_rating'])
        worksheet.write(row, 2, actor['count'])
        row += 1

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="actor_ratings_report.xlsx"'
    return response
