from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('scanner/', views.barcode_scanner, name='barcode_scanner'),
    path('check-attendance/', views.check_attendance, name='check_attendance'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('students/create/', views.create_student, name='create_student'),
    path('students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:student_id>/update/', views.update_student, name='update_student'),
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('students/<int:student_id>/qr-code/', views.student_qr_code, name='student_qr_code'),
    path('qr-codes/', views.generate_all_qr_codes, name='generate_all_qr_codes'),
    path('guardians/', views.guardian_list, name='guardian_list'),
    path('guardians/create/', views.create_guardian, name='create_guardian'),
    path('guardians/<int:guardian_id>/edit/', views.edit_guardian, name='edit_guardian'),
    path('guardians/<int:guardian_id>/update/', views.update_guardian, name='update_guardian'),
    path('guardians/<int:guardian_id>/delete/', views.delete_guardian, name='delete_guardian'),
]
