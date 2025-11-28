# Automated Attendance Management Features

## Overview
This document describes the automated attendance management features and new enhancements added to the Django Management System.

## Features Implemented

### 1. Automated Attendance Sheet Generation
Automatically generates attendance sheets for classes based on their scheduled time.

**How it works:**
- Each Grade/Class has a `reset_time` field indicating when lessons start
- Each Grade/Class has a `lesson_duration` field (in hours) indicating how long the lesson lasts
- The system automatically generates attendance sheets when it's time for a lesson
- Students are automatically added to the attendance sheet

**Management Command:**
```bash
python manage.py generate_attendance
```

Options:
- `--force`: Force generation even if attendance already exists

**Automated Execution:**
The system uses Django background tasks to automatically run this command every 5 minutes to check if any class should have attendance generated.

### 2. Auto-Save Attendance After Lesson
Automatically saves attendance records to history after the lesson duration has elapsed.

**How it works:**
- After the lesson duration (e.g., 2 or 3 hours) has passed since attendance was generated
- The system automatically saves the attendance to history
- Clears the current attendance sheet
- Updates student presence/absence counts

**Management Command:**
```bash
python manage.py autosave_attendance
```

Options:
- `--force`: Force save all existing attendance sheets immediately

**Automated Execution:**
The system uses Django background tasks to automatically run this command every 10 minutes to check if any attendance sheets should be saved.

### 3. Student ID Generation
Automatically generates unique student IDs when a student is created.

**ID Format:** `YYYYMMDD-RRRRR`
- `YYYYMMDD`: Date the student joined (e.g., 20231215)
- `RRRRR`: Random 5-digit number (e.g., 12345)
- Example: `20231215-12345`

**How it works:**
- When a new student is created, the system automatically generates a unique student ID
- The ID is based on the `date_joined` field plus random numbers
- Ensures no duplicate IDs exist in the system

### 4. Phone Number Validation
Phone numbers must be exactly 10 digits.

**Features:**
- HTML5 pattern validation
- JavaScript validation to allow only digits
- Automatic truncation if more than 10 digits are entered
- Applied to both Student and Guardian forms

### 5. Map Integration for Address Selection
Interactive map for selecting addresses when adding/editing students.

**Features:**
- Click on map to select a location
- Search for locations by name
- Automatic reverse geocoding to get full address
- Uses OpenStreetMap and Leaflet.js
- Free and open-source solution

**How to use:**
1. Click "Select on Map" button next to the address field
2. Search for a location or click directly on the map
3. Click "Confirm Address" to use the selected location

### 6. Date Format (DD/MM/YYYY)
Date format changed from MM/DD/YYYY to DD/MM/YYYY throughout the application.

**Features:**
- Automatic formatting as you type
- Pattern validation
- Applied to birth date and other date fields

## Setup Instructions

### 1. Apply Migrations
```bash
python manage.py migrate
```

### 2. Set Up Background Tasks
To enable automated attendance generation and auto-save:

```bash
# Set up the recurring tasks
python manage.py setup_attendance_tasks

# Start the background task processor (in a separate terminal or as a service)
python manage.py process_tasks
```

**Note:** In production, you should run `process_tasks` as a system service or use a process manager like systemd or supervisord.

### 3. Configure Grades
Make sure each grade has:
- A `reset_time` set to when the lesson starts (e.g., 14:00 for 2 PM)
- A `lesson_duration` set to how long the lesson lasts (e.g., 2 or 3 hours)

## Manual Usage

### Generate Attendance Manually
If you need to generate attendance sheets outside of the automated schedule:

```bash
python manage.py generate_attendance --force
```

### Save Attendance Manually
If you need to save attendance sheets before the lesson duration has elapsed:

```bash
python manage.py autosave_attendance --force
```

## Database Fields Added

### Student Model
- `date_joined`: DateField - When the student joined (default: today)
- `student_id`: CharField - Unique auto-generated student ID

### Grade Model
- `lesson_duration`: IntegerField - Lesson duration in hours (default: 2)

## API Changes

### Student Creation
When creating a student, the following fields are now handled:
- `birth_date`: Accepts DD/MM/YYYY format
- `student_id`: Auto-generated (don't need to provide)
- `date_joined`: Auto-set to today (can be overridden)

### Phone Number Validation
- Students and Guardians: Phone numbers must be exactly 10 digits
- Validation happens both client-side (HTML5 + JavaScript) and server-side (Django model validators)

## Troubleshooting

### Background Tasks Not Running
1. Make sure you've run `python manage.py setup_attendance_tasks`
2. Ensure `python manage.py process_tasks` is running
3. Check if `django-background-tasks` is installed: `pip install django-background-tasks`

### Attendance Not Auto-Generating
1. Check that grades have `reset_time` configured
2. Verify that students are assigned to the grade
3. Check that students are marked as `active=True`
4. Run manually with `--force` flag to debug

### Map Not Loading
1. Ensure internet connection is available (uses CDN for Leaflet.js and OpenStreetMap tiles)
2. Check browser console for JavaScript errors
3. Verify that the modal is properly initialized

## Future Enhancements

Possible future improvements:
- Email notifications when attendance is auto-saved
- Dashboard to view automated task status
- Configurable schedule for different days/times
- SMS notifications for absent students
- Parent portal to view attendance history
