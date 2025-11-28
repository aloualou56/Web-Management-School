from django.core.management.base import BaseCommand
from django.utils import timezone
from Class_related.models import Grade, Attendance, AttendanceHistory
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Auto-save attendance sheets after lesson duration has passed'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force save all existing attendance sheets',
        )

    def handle(self, *args, **options):
        """
        Save and clear attendance sheets for grades whose lesson duration has elapsed
        """
        force = options.get('force', False)
        now = timezone.now()
        
        # Get all grades
        grades = Grade.objects.all()
        
        for grade in grades:
            # Check if there are any attendance records for this grade
            attendances = Attendance.objects.filter(grade=grade)
            
            if not attendances.exists():
                continue
            
            # Get the oldest attendance timestamp for this grade
            oldest_attendance = attendances.order_by('timestamp').first()
            
            if not oldest_attendance or not oldest_attendance.timestamp:
                continue
            
            # Calculate elapsed time since attendance was created
            elapsed_time = now - oldest_attendance.timestamp
            lesson_duration_hours = grade.lesson_duration
            
            # Check if lesson duration has passed (or force save)
            if elapsed_time >= timedelta(hours=lesson_duration_hours) or force:
                # Prepare attendance records for history
                attendance_records = []
                for record in attendances:
                    if record.student:
                        attendance_records.append({
                            'first_name': record.student.first_name,
                            'last_name': record.student.last_name,
                            'present': record.present,
                        })
                        # Update student presence/absence counts
                        if record.present:
                            record.student.presences += 1
                        else:
                            record.student.absences += 1
                        record.student.save()
                
                # Create history record
                if attendance_records:
                    AttendanceHistory.objects.create(
                        attendance_records=attendance_records,
                        grade=grade,
                        attendance_date=oldest_attendance.timestamp.date()
                    )
                
                # Delete current attendance records
                attendances.delete()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully saved and cleared attendance for {grade.name}. '
                        f'Elapsed time: {elapsed_time.total_seconds() / 3600:.1f} hours. '
                        f'Saved {len(attendance_records)} records to history.'
                    )
                )
