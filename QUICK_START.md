# Quick Start Guide - New Features

## 🎉 What's New

### 1. Student IDs Are Now Auto-Generated!
When you create a new student, they automatically get a unique ID like: **20251120-34059**
- The first part (20251120) is the date they joined
- The second part (34059) is a random number to ensure uniqueness

### 2. Phone Numbers Must Be Exactly 10 Digits
- The system will only accept phone numbers with exactly 10 digits
- No country codes, no spaces, no dashes - just 10 digits
- Works for both students and guardians

### 3. Select Address on a Map!
When adding or editing a student:
1. Click the "Select on Map" button next to the address field
2. Search for a location OR click directly on the map
3. The address will be automatically filled in
4. You can also still type the address manually if you prefer

### 4. Dates Use DD/MM/YYYY Format
All dates throughout the system now use the format: Day/Month/Year
- Example: 20/11/2025 (20th November 2025)
- Much more natural for most countries!

### 5. Automated Attendance Management
The system can now automatically:
- Generate attendance sheets when it's time for class
- Save attendance to history after the lesson ends (2-3 hours later)
- Keep track of everything without manual intervention

## 🚀 Setting Up Automated Attendance

### Step 1: Configure Your Grades/Classes
For each grade, make sure you set:
1. **Reset Time**: When does the class start? (e.g., 14:00 for 2 PM)
2. **Lesson Duration**: How long is the class? (2 or 3 hours)

You can do this in the Django admin panel or through the grades page.

### Step 2: Set Up Background Tasks (One-Time Setup)
Run these commands in your terminal:

```bash
# Apply database changes
python manage.py migrate

# Set up automated tasks
python manage.py setup_attendance_tasks

# Start the background processor (keep this running)
python manage.py process_tasks
```

### Step 3: That's It!
The system will now:
- Check every 5 minutes if any class should start → generates attendance sheet
- Check every 10 minutes if any class has ended → saves to history

## 📱 Using the New Features

### Adding a Student with Map
1. Go to Students page
2. Click "Add Student"
3. Fill in the basic info
4. For address: Click "Select on Map"
5. Search for the location or click on the map
6. Click "Confirm Address"
7. Phone must be exactly 10 digits (no spaces!)
8. Birth date format: DD/MM/YYYY (e.g., 15/03/2010)
9. Save - student ID will be generated automatically!

### Checking Student ID
After saving, you'll see the student ID displayed in the table:
- Old way: #00042 (just a number)
- New way: 20251120-34059 (date-based unique ID)

### Manual Attendance Commands
If you need to do something manually:

```bash
# Generate attendance sheets right now (ignoring schedule)
python manage.py generate_attendance --force

# Save all current attendance sheets to history
python manage.py autosave_attendance --force
```

## ⚠️ Important Notes

### Phone Numbers
- Must be EXACTLY 10 digits
- Examples of what WON'T work:
  - ❌ 123-456-7890 (has dashes)
  - ❌ +1 1234567890 (has country code)
  - ❌ 123 456 7890 (has spaces)
  - ❌ 12345678 (only 8 digits)
- Example of what WILL work:
  - ✅ 1234567890

### Dates
- Always use DD/MM/YYYY format
- Examples:
  - ✅ 20/11/2025
  - ✅ 01/01/2024
  - ❌ 11/20/2025 (this is MM/DD/YYYY - American format)

### Map Features
- Requires internet connection (uses OpenStreetMap)
- You can still type addresses manually if the map doesn't work
- The map helps ensure addresses are properly formatted

## 🐛 Troubleshooting

### "Background tasks aren't running"
Make sure `python manage.py process_tasks` is running. This should be running constantly in the background.

### "Map not loading"
- Check your internet connection
- Try refreshing the page
- You can still type the address manually

### "Phone number won't save"
Make sure it's exactly 10 digits with no extra characters.

### "Date format error"
Use DD/MM/YYYY format (e.g., 20/11/2025, not 11/20/2025)

## 📖 More Information
See `ATTENDANCE_FEATURES.md` for detailed technical documentation.
