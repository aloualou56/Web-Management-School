from django.core.management.base import BaseCommand
from django.utils import timezone
from Class_related.models import Grade, Attendance
from People.models import Student
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Auto-generate attendance sheets for grades based on their schedule (weekdays, class_time) and reset_time'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force generation even if attendance already exists',
        )

    def handle(self, *args, **options):
        """
        Generate attendance sheets for grades based on their schedule.
        Checks both reset_time and class schedule (weekdays and class_time).
        """
        force = options.get('force', False)
        now = timezone.now()
        current_time = now.time()
        
        # Map weekday index to Grade.WEEKDAY_CHOICES format
        weekday_map = {
            0: 'MONDAY',
            1: 'TUESDAY',
            2: 'WEDNESDAY',
            3: 'THURSDAY',
            4: 'FRIDAY',
            5: 'SATURDAY',
            6: 'SUNDAY',
        }
        current_weekday = weekday_map[now.weekday()]
        
        # Get all grades
        grades = Grade.objects.all()
        
        for grade in grades:
            should_generate = False
            reason = ""
            
            # Check if grade has a schedule defined (weekdays and class_time)
            if grade.weekdays and grade.class_time:
                weekdays_list = grade.get_weekdays_list()
                
                # Check if today is a scheduled day
                if current_weekday in weekdays_list:
                    # Check if current time is within 5 minutes of the class_time
                    class_datetime = datetime.combine(now.date(), grade.class_time)
                    time_diff = abs((datetime.combine(now.date(), current_time) - class_datetime).total_seconds())
                    
                    if time_diff <= 300:  # Within 5-minute window
                        should_generate = True
                        reason = f"scheduled class time {grade.class_time} on {current_weekday}"
            
            # Fallback to reset_time if no schedule is defined
            if not should_generate:
                reset_datetime = datetime.combine(now.date(), grade.reset_time)
                time_diff = abs((datetime.combine(now.date(), current_time) - reset_datetime).total_seconds())
                
                # Within 5-minute window (300 seconds)
                if time_diff <= 300:
                    should_generate = True
                    reason = f"reset time {grade.reset_time}"
            
            # Generate attendance if conditions are met or force is enabled
            if should_generate or force:
                # Check if attendance already exists for this grade
                existing_attendance = Attendance.objects.filter(grade=grade).exists()
                
                if existing_attendance and not force:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Attendance for {grade.name} already exists. Skipping.'
                        )
                    )
                    continue
                
                # Get all active students in this grade
                students = Student.objects.filter(grade=grade, active=True)
                
                if not students.exists():
                    self.stdout.write(
                        self.style.WARNING(
                            f'No active students found for {grade.name}. Skipping.'
                        )
                    )
                    continue
                
                # Create attendance records for all students
                attendance_records = [
                    Attendance(student=student, grade=grade, present=False)
                    for student in students
                ]
                Attendance.objects.bulk_create(attendance_records)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully generated attendance sheet for {grade.name} '
                        f'with {len(attendance_records)} students at {now.strftime("%A %H:%M")} '
                        f'(triggered by {reason})'
                    )
                )
