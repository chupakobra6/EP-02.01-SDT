from django.urls import path, include

from Theater.views import home, all_performances, review_page, login_view, logout_view, profile_view, seats_view, \
    create_ticket, employees_list, employee_create, employee_edit, employee_delete, halls_list, hall_create, hall_edit, \
    hall_delete, seats_list, seat_create, seat_edit, seat_delete, actors_list, actor_create, actor_edit, actor_delete, \
    performances_list, performance_create, performance_edit, performance_delete, passport_data_list, \
    passport_data_create, passport_data_edit, passport_data_delete, performance_actor_create, performance_actor_edit, \
    performance_actor_delete, tickets_list, ticket_create, ticket_edit, ticket_delete, positions_list, position_create, \
    position_edit, position_delete, performance_rating_list, performance_rating_create, performance_rating_edit, \
    performance_rating_delete, actor_rating_list, actor_rating_create, actor_rating_edit, actor_rating_delete, \
    performance_actor_list, export_tickets_report, export_performance_ratings_report, export_actor_ratings_report

cassier = [
    path('seats/', seats_view, name='seats_view'),
    path('create_ticket/', create_ticket, name='create_ticket'),
]

director = [
    path('employees/', employees_list, name='employees_list'),
    path('employees/create/', employee_create, name='employee_create'),
    path('employees/edit/<int:pk>/', employee_edit, name='employee_edit'),
    path('employees/delete/<int:pk>/', employee_delete, name='employee_delete'),

    path('halls/', halls_list, name='halls_list'),
    path('halls/create/', hall_create, name='hall_create'),
    path('halls/edit/<int:pk>/', hall_edit, name='hall_edit'),
    path('halls/delete/<int:pk>/', hall_delete, name='hall_delete'),

    path('seats/', seats_list, name='seats_list'),
    path('seats/create/', seat_create, name='seat_create'),
    path('seats/edit/<int:pk>/', seat_edit, name='seat_edit'),
    path('seats/delete/<int:pk>/', seat_delete, name='seat_delete'),

    path('actors/', actors_list, name='actors_list'),
    path('actors/create/', actor_create, name='actor_create'),
    path('actors/edit/<int:pk>/', actor_edit, name='actor_edit'),
    path('actors/delete/<int:pk>/', actor_delete, name='actor_delete'),

    path('performances/', performances_list, name='performances_list'),
    path('performances/create/', performance_create, name='performance_create'),
    path('performances/edit/<int:pk>/', performance_edit, name='performance_edit'),
    path('performances/delete/<int:pk>/', performance_delete, name='performance_delete'),

    path('passport-data/', passport_data_list, name='passport_data_list'),
    path('passport-data/create/', passport_data_create, name='passport_data_create'),
    path('passport-data/edit/<int:pk>/', passport_data_edit, name='passport_data_edit'),
    path('passport-data/delete/<int:pk>/', passport_data_delete, name='passport_data_delete'),

    path('performance-actors/', performance_actor_list, name='performance_actors_list'),
    path('performance-actors/create/', performance_actor_create, name='performance_actor_create'),
    path('performance-actors/edit/<int:pk>/', performance_actor_edit, name='performance_actor_edit'),
    path('performance-actors/delete/<int:pk>/', performance_actor_delete, name='performance_actor_delete'),

    path('actor-ratings/', actor_rating_list, name='actor_ratings_list'),
    path('actor-ratings/create/', actor_rating_create, name='actor_rating_create'),
    path('actor-ratings/edit/<int:pk>/', actor_rating_edit, name='actor_rating_edit'),
    path('actor-ratings/delete/<int:pk>/', actor_rating_delete, name='actor_rating_delete'),

    path('performance-ratings/', performance_rating_list, name='performance_ratings_list'),
    path('performance-ratings/create/', performance_rating_create, name='performance_rating_create'),
    path('performance-ratings/edit/<int:pk>/', performance_rating_edit, name='performance_rating_edit'),
    path('performance-ratings/delete/<int:pk>/', performance_rating_delete, name='performance_rating_delete'),

    path('positions/', positions_list, name='positions_list'),
    path('positions/create/', position_create, name='position_create'),
    path('positions/edit/<int:pk>/', position_edit, name='position_edit'),
    path('positions/delete/<int:pk>/', position_delete, name='position_delete'),

    path('tickets/', tickets_list, name='tickets_list'),
    path('tickets/create/', ticket_create, name='ticket_create'),
    path('tickets/edit/<int:pk>/', ticket_edit, name='ticket_edit'),
    path('tickets/delete/<int:pk>/', ticket_delete, name='ticket_delete'),
]

urlpatterns = [
    path('', home, name='home'),
    path('performances/', all_performances, name='all_performances'),
    path('reviews/', review_page, name='review_page'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),

    path('cassier/', include(cassier)),
    path('director/', include(director)),

    path('export/tickets/', export_tickets_report, name='export_tickets'),
    path('export/performance_ratings/', export_performance_ratings_report, name='export_performance_ratings'),
    path('export/actor_ratings/', export_actor_ratings_report, name='export_actor_ratings'),
]
