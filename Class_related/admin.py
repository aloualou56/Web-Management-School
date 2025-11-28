from django.contrib import admin
from django import forms
from django.urls import path
from django.utils.translation import gettext_lazy as _
from .models import Grade, Attendance, AttendanceHistory
from People.models import Student

class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'reset_time', 'class_time', 'lesson_duration', 'weekdays', 'student_list')
    list_editable = ('reset_time', 'class_time', 'lesson_duration')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'reset_time')
        }),
        (_('Class Schedule'), {
            'fields': ('class_time', 'lesson_duration', 'weekdays'),
            'description': _('Define the class schedule for automatic attendance generation')
        }),
    )

    def student_list(self, obj):
        students = Student.objects.filter(grade=obj)
        return ", ".join([str(student) for student in students])
    student_list.short_description = _('Students')

class AttendanceForm(forms.ModelForm):
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), required=True, label=_("Grade"))

    class Meta:
        model = Attendance
        fields = ['grade']

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected_grade = self.cleaned_data['grade']
        students = Student.objects.filter(grade=selected_grade, active=True)
        
        attendance_records = [
            Attendance(student=student, grade=selected_grade, present=False)
            for student in students
        ]
        Attendance.objects.bulk_create(attendance_records)
        return instance

class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceForm
    list_display = ('student', 'grade', 'present', 'timestamp')
    list_filter = ('grade', 'present')

    def save_attendance_list(self, request, queryset):
        attendance_records = []
        grade = None
        for obj in queryset:
            attendance_records.append({
                'first_name': obj.student.first_name,
                'last_name': obj.student.last_name,
                'present': obj.present,
            })
            grade = obj.grade
        
        if grade:
            AttendanceHistory.objects.create(attendance_records=attendance_records, grade=grade)
            self.message_user(request, _("Attendance list saved successfully."))
        else:
            self.message_user(request, _("No grade found to save."), level="error")

    actions = [save_attendance_list]

    def has_add_permission(self, request):
        return True

    def save_model(self, request, obj, form, change):
        pass

class AttendanceHistoryAdmin(admin.ModelAdmin):
    list_display = ('attendance_date', 'grade', 'present_students_list', 'absent_students_list')

    def present_students_list(self, obj):
        return ", ".join(obj.present_students)
    present_students_list.short_description = _('Present Students')

    def absent_students_list(self, obj):
        return ", ".join(obj.absent_students)
    absent_students_list.short_description = _('Absent Students')

admin.site.register(Grade, GradeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(AttendanceHistory, AttendanceHistoryAdmin)
