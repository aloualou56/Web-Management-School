"""
Background tasks for automated attendance management.

This module contains functions that are scheduled to run periodically
using django-background-tasks to automate attendance sheet generation
and saving.
"""
from background_task import background
from django.core import management
import logging

logger = logging.getLogger(__name__)


@background(schedule=0)
def generate_attendance_sheets():
    """
    Background task to generate attendance sheets for grades.
    This should be scheduled to run every few minutes to check if
    any grade's reset_time has been reached.
    """
    try:
        management.call_command('generate_attendance')
        logger.info('Successfully ran generate_attendance command')
    except Exception as e:
        logger.error(f'Error running generate_attendance: {e}')


@background(schedule=0)
def autosave_attendance_sheets():
    """
    Background task to auto-save attendance sheets after lesson duration.
    This should be scheduled to run periodically to check if any
    attendance sheets should be saved.
    """
    try:
        management.call_command('autosave_attendance')
        logger.info('Successfully ran autosave_attendance command')
    except Exception as e:
        logger.error(f'Error running autosave_attendance: {e}')
