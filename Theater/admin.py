from django.contrib import admin

from Theater.models import Position, PassportData, Employee, Hall, Seat, Actor, Performance, Ticket, PerformanceActor, \
    ActorRating, PerformanceRating


# Register your models here.
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(PassportData)
class PassportDataAdmin(admin.ModelAdmin):
    list_display = ['series', 'number', 'place_of_issue', 'date_of_issue']
    search_fields = ['series', 'number']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'patronymic', 'position', 'passport_data']
    list_display_links = ['name', 'surname']
    list_filter = ['position']
    search_fields = ['name', 'surname', 'patronymic']


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['title', 'number_of_rows', 'number_of_seats']
    search_fields = ['title']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['hall', 'row_count', 'seat_number', 'status', 'price']
    list_filter = ['hall', 'status']
    search_fields = ['hall__title', 'row_count', 'seat_number']


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'patronymic', 'role']
    list_display_links = ['name', 'surname']
    search_fields = ['name', 'surname', 'role']


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'hall']
    list_filter = ['date', 'hall']
    search_fields = ['title']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'patronymic', 'performance', 'hall', 'seat', 'order_date', 'price']
    list_filter = ['order_date', 'performance', 'hall']
    search_fields = ['name', 'surname', 'performance__title']


@admin.register(PerformanceActor)
class PerformanceActorAdmin(admin.ModelAdmin):
    list_display = ['performance', 'actor']
    list_filter = ['performance', 'actor']
    search_fields = ['performance__title', 'actor__name']


@admin.register(ActorRating)
class ActorRatingAdmin(admin.ModelAdmin):
    list_display = ['actor', 'grade', 'description']
    list_filter = ['actor', 'grade']
    search_fields = ['actor__name', 'description']


@admin.register(PerformanceRating)
class PerformanceRatingAdmin(admin.ModelAdmin):
    list_display = ['performance', 'grade', 'description']
    list_filter = ['performance', 'grade']
    search_fields = ['performance__title', 'description']
