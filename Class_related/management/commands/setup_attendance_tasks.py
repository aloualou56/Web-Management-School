from django.core.management.base import BaseCommand
from background_task.models import Task
from Class_related.tasks import generate_attendance_sheets, autosave_attendance_sheets


class Command(BaseCommand):
    help = 'Set up recurring background tasks for attendance automation'

    def handle(self, *args, **options):
        """
        Set up recurring tasks for attendance generation and auto-save.
        These tasks will run periodically to automate attendance management.
        """
        # Clear existing tasks to avoid duplicates
        Task.objects.filter(task_name__contains='Class_related.tasks').delete()
        
        # Schedule generate_attendance to run every 5 minutes
        # This checks if any grade's reset_time has been reached
        generate_attendance_sheets(repeat=300, repeat_until=None)  # 300 seconds = 5 minutes
        
        # Schedule autosave_attendance to run every 10 minutes
        # This checks if any attendance sheets should be saved
        autosave_attendance_sheets(repeat=600, repeat_until=None)  # 600 seconds = 10 minutes
        
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully set up recurring tasks:\n'
                '- generate_attendance_sheets: every 5 minutes\n'
                '- autosave_attendance_sheets: every 10 minutes\n\n'
                'Run "python manage.py process_tasks" to start the background task processor.'
            )
        )
