from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from People.models import Student

class Grade(models.Model):
    """
    Represents a grade or class in the school.
    """
    WEEKDAY_CHOICES = [
        ('MONDAY', _('Monday')),
        ('TUESDAY', _('Tuesday')),
        ('WEDNESDAY', _('Wednesday')),
        ('THURSDAY', _('Thursday')),
        ('FRIDAY', _('Friday')),
        ('SATURDAY', _('Saturday')),
        ('SUNDAY', _('Sunday')),
    ]
    
    name = models.CharField(max_length=40, verbose_name=_("Name"))
    reset_time = models.TimeField(verbose_name=_("Reset Time"))
    lesson_duration = models.IntegerField(default=2, verbose_name=_("Lesson Duration (hours)"))
    weekdays = models.CharField(max_length=100, blank=True, verbose_name=_("Weekdays"), help_text=_("Comma-separated weekdays (e.g., MONDAY,WEDNESDAY,FRIDAY)"))
    class_time = models.TimeField(null=True, blank=True, verbose_name=_("Class Time"), help_text=_("Time when the class starts"))

    def __str__(self):
        return self.name
    
    def get_weekdays_list(self):
        """Return a list of weekdays for this class."""
        if self.weekdays:
            return [day.strip() for day in self.weekdays.split(',')]
        return []
    
    def get_weekdays_display(self):
        """Return a formatted string of weekdays."""
        weekday_map = dict(self.WEEKDAY_CHOICES)
        days = self.get_weekdays_list()
        return ', '.join([str(weekday_map.get(day, day)) for day in days])

    class Meta:
        verbose_name = _('Grade')
        verbose_name_plural = _('Grades')

class Attendance(models.Model):
    """
    Represents a student's attendance record for a specific grade.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name=_("Student"), null=True)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, verbose_name=_("Grade"), related_name='attendances', null=True, blank=True)
    present = models.BooleanField(default=False, verbose_name=_("Present"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Timestamp"), null=True)

    def __str__(self):
        if self.student:
            return f'{self.student} - {self.grade}'
        return f'Unknown Student - {self.grade}'


    def save(self, *args, **kwargs):
        if not self.pk:
            if self.student:
                if self.present:
                    self.student.presences += 1
                else:
                    self.student.absences += 1
                self.student.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')

class AttendanceHistory(models.Model):
    """
    Stores a history of attendance records for a specific grade.
    """
    attendance_date = models.DateField(default=timezone.now, verbose_name=_("Attendance Date"))
    attendance_records = models.JSONField(verbose_name=_("Attendance Records"))
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, verbose_name=_("Grade"), related_name='history_attendances', null=True, blank=True)

    def __str__(self):
        return self.attendance_date.strftime('%Y-%m-%d')

    @property
    def present_students(self):
        return [f"{record['first_name']} {record['last_name']}" for record in self.attendance_records if record['present']]

    @property
    def absent_students(self):
        return [f"{record['first_name']} {record['last_name']}" for record in self.attendance_records if not record['present']]

    class Meta:
        verbose_name = _("Attendance History")
        verbose_name_plural = _("Attendance History")
        ordering = ['-attendance_date']
