from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils.translation import gettext_lazy as _, ngettext
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core import management
from datetime import datetime
from functools import wraps
import os
import logging
from .models import Grade, Attendance, AttendanceHistory
from People.models import Student

logger = logging.getLogger(__name__)

def require_api_token(view_func):
    """Decorator to require ATTENDANCE_API_TOKEN for API endpoints"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        expected_token = os.environ.get('ATTENDANCE_API_TOKEN')
        
        if not expected_token:
            return JsonResponse({'error': 'Server configuration error: ATTENDANCE_API_TOKEN not set'}, status=500)
        
        if not auth_header.startswith('Bearer ') or auth_header[7:] != expected_token:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def attendance_history(request):
    grades = Grade.objects.all()
    selected_grade_id = request.GET.get('grade')
    
    if selected_grade_id:
        history = AttendanceHistory.objects.filter(grade_id=selected_grade_id)
    else:
        history = AttendanceHistory.objects.none()

    context = {
        'grades': grades,
        'history': history,
        'selected_grade_id': selected_grade_id,
    }
    return render(request, 'attendance_history.html', context)

@login_required
def attendance_list(request):
    attendances = Attendance.objects.select_related('grade', 'student').order_by('grade')
    grouped_attendances = {}
    for attendance in attendances:
        grade = attendance.grade
        if grade not in grouped_attendances:
            grouped_attendances[grade] = {
                'attendances': [],
                'present_count': 0,
                'absent_count': 0
            }
        grouped_attendances[grade]['attendances'].append(attendance)
        if attendance.present:
            grouped_attendances[grade]['present_count'] += 1
        else:
            grouped_attendances[grade]['absent_count'] += 1

    context = {
        'grouped_attendances': grouped_attendances,
        'grades': Grade.objects.all(),
    }
    return render(request, 'attendances.html', context)

@login_required
def add_attendance(request):
    if request.method == 'POST':
        grade_id = request.POST.get('grade')
        grade = get_object_or_404(Grade, id=grade_id)
        students = Student.objects.filter(grade=grade, active=True)
        
        attendance_records = [
            Attendance(student=student, grade=grade, present=False)
            for student in students
        ]
        Attendance.objects.bulk_create(attendance_records)
        return redirect('class_related:attendance_list')
    return redirect('class_related:attendance_list')

@login_required
def delete_attendance(request, grade_id):
    if request.method == 'POST':
        grade = get_object_or_404(Grade, id=grade_id)
        attendances = Attendance.objects.filter(grade=grade)

        attendance_records = []
        for record in attendances:
            attendance_records.append({
                'first_name': record.student.first_name,
                'last_name': record.student.last_name,
                'present': record.present,
            })
            if record.present:
                record.student.presences += 1
            else:
                record.student.absences += 1
            record.student.save()

        AttendanceHistory.objects.create(
            attendance_records=attendance_records,
            grade=grade
        )
        attendances.delete()
        return redirect('class_related:attendance_list')
    return redirect('class_related:attendance_list')

@login_required
def grade_list(request):
    grades = Grade.objects.all()
    unassigned_students = Student.objects.filter(grade__isnull=True)
    context = {
        'grades': grades,
        'unassigned_students': unassigned_students
    }
    return render(request, 'grades.html', context)

@login_required
def create_grade(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        reset_time = request.POST.get('reset_time')
        class_time = request.POST.get('class_time')
        lesson_duration = request.POST.get('lesson_duration', 2)
        weekdays = request.POST.get('weekdays', '')
        
        Grade.objects.create(
            name=name,
            reset_time=reset_time,
            class_time=class_time if class_time else None,
            lesson_duration=lesson_duration,
            weekdays=weekdays
        )
    return redirect('class_related:grade_list')

@login_required
def delete_grade(request, grade_id):
    if request.method == 'POST':
        grade = get_object_or_404(Grade, id=grade_id)
        # Use transaction to ensure atomicity
        with transaction.atomic():
            # Unassign students from the grade and get count
            student_count = Student.objects.filter(grade=grade).update(grade=None)
            # Delete the grade
            grade.delete()
        # Show success message
        if student_count > 0:
            message = ngettext(
                '%(count)d student was unassigned from the grade.',
                '%(count)d students were unassigned from the grade.',
                student_count
            ) % {'count': student_count}
            messages.success(request, message)
        else:
            messages.success(request, _('Grade deleted successfully.'))
    return redirect('class_related:grade_list')

@login_required
def assign_student(request, grade_id):
    if request.method == 'POST':
        grade = get_object_or_404(Grade, id=grade_id)
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        student.grade = grade
        student.save()
    return redirect('class_related:grade_list')

@login_required
def remove_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.grade = None
    student.save()
    return redirect('class_related:grade_list')

def server_time(request):
    """API endpoint to get current server time in UTC"""
    now = datetime.utcnow()
    weekday_name = now.strftime('%a')
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    return JsonResponse({
        'time': formatted_time,
        'weekday': weekday_name,
        'full_display': f"{weekday_name}, {now.strftime('%d %b %Y')} - {now.strftime('%H:%M:%S')} UTC"
    })

@csrf_exempt
@require_POST
@require_api_token
def trigger_attendance_generation(request):
    """API endpoint to trigger attendance generation"""
    try:
        management.call_command('generate_attendance')
        return JsonResponse({'status': 'success', 'message': 'Attendance generation triggered'})
    except Exception as e:
        logger.error(f'Error triggering attendance generation: {e}', exc_info=True)
        return JsonResponse({'error': 'Failed to trigger attendance generation'}, status=500)

@csrf_exempt
@require_POST
@require_api_token
def trigger_attendance_autosave(request):
    """API endpoint to trigger attendance autosave"""
    try:
        management.call_command('autosave_attendance')
        return JsonResponse({'status': 'success', 'message': 'Attendance autosave triggered'})
    except Exception as e:
        logger.error(f'Error triggering attendance autosave: {e}', exc_info=True)
        return JsonResponse({'error': 'Failed to trigger attendance autosave'}, status=500)
