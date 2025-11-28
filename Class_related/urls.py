from django.urls import path
from . import views

app_name = 'class_related'

urlpatterns = [
    path('api/server-time/', views.server_time, name='server_time'),
    path('api/trigger-attendance-generation/', views.trigger_attendance_generation, name='trigger_attendance_generation'),
    path('api/trigger-attendance-autosave/', views.trigger_attendance_autosave, name='trigger_attendance_autosave'),
    path('attendances/', views.attendance_list, name='attendance_list'),
    path('attendances/add/', views.add_attendance, name='add_attendance'),
    path('attendances/delete/<int:grade_id>/', views.delete_attendance, name='delete_attendance'),
    path('attendances/history/', views.attendance_history, name='attendance_history'),
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/create/', views.create_grade, name='create_grade'),
    path('grades/<int:grade_id>/delete/', views.delete_grade, name='delete_grade'),
    path('grades/<int:grade_id>/assign_student/', views.assign_student, name='assign_student'),
    path('students/<int:student_id>/remove/', views.remove_student, name='remove_student'),
]
