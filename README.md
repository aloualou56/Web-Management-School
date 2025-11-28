# Django Management System

A comprehensive Django-based school/class management system for managing students, guardians, classes, attendance, and payments. This application can be deployed on Vercel, Render, or locally.

## 🚀 Live Demo

Try out the application with a live demo:

**Demo URL:** [https://django-management.onrender.com](https://django-management.onrender.com)

**Demo Credentials:**
- **Username:** `demo`
- **Password:** `demo123`

> **Note:** The demo is hosted on Render's free tier, so it may take a few seconds to wake up if it hasn't been used recently. Feel free to explore all features!

---

## ✨ Features

### 👨‍🎓 Student Management
- Add, edit, and delete student records
- Auto-generated unique student IDs (format: YYYYMMDD-RRRRR)
- Student photos and profile management
- Phone number validation (10 digits)
- Link students to guardians and classes
- Track student presence/absence statistics
- Search functionality with multi-field filtering

### 👨‍👩‍👧 Guardian Management
- Manage guardian information (parents/contacts)
- Link guardians to multiple students
- Contact details including phone, email, and address
- Interactive map for address selection using OpenStreetMap

### 🏫 Class/Grade Management
- Create and manage classes/grades
- Configure class schedules (weekdays and time)
- Set lesson duration for each class
- View students assigned to each class
- Unassigned students alert banner

### 📋 Attendance Tracking
- Manual attendance marking with presence/absence
- Attendance history with date filtering
- QR code scanning for quick attendance
- Auto-save attendance records after lesson duration
- View attendance statistics per student

### 🤖 Automated Attendance (GitHub Actions)
- Automatic attendance sheet generation based on class schedules
- Auto-save attendance after lesson duration
- Runs every 5 minutes via GitHub Actions (free!)
- No paid background workers required

### 💰 Payment Management
- Create payment plans with one-time and monthly fees
- Track payments per student
- Generate and manage receipts
- Academic year tracking
- Automatic monthly fee calculation

### 🔐 User Authentication
- Secure login system
- "Remember me" functionality
- Session management
- Protected routes with login required

### 📱 Responsive Design
- Mobile-friendly interface
- Bootstrap 5 styling
- Dark sidebar navigation
- Real-time server clock display

### 🌍 Internationalization
- Multi-language support (English and Greek)
- Date format: DD/MM/YYYY
- Translatable labels and messages

---

## 🤖 Automatic Attendance (GitHub Actions)

This project uses GitHub Actions to automatically generate and save attendance sheets every 5 minutes - completely free!

### How it works:
- GitHub Actions triggers attendance commands via API
- Runs every 5 minutes automatically
- No paid services or background workers required
- Works perfectly with Render's free tier

### Setup:
See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed instructions.

---

## English

### Deploy to Vercel

**Important:** Vercel requires an external database. SQLite is not supported in production on Vercel. You must use an external database service like:
- [Neon](https://neon.tech/) (PostgreSQL - Free tier available)
- [PlanetScale](https://planetscale.com/) (MySQL - Free tier available)
- [Supabase](https://supabase.com/) (PostgreSQL - Free tier available)
- [Railway](https://railway.app/) (PostgreSQL)

#### Quick Deployment

Click below for quick deployment in Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Faloualou56%2Fdjango_management)

#### Manual Setup

1. Fork this repository to your GitHub account
2. Set up an external PostgreSQL database (e.g., on Neon, Supabase, or Railway)
3. Go to [Vercel Dashboard](https://vercel.com/dashboard)
4. Click "Add New..." → "Project"
5. Import your forked repository
6. Configure environment variables:
   - `SECRET_KEY`: Generate a secure secret key
   - `DEBUG`: Set to `False`
   - `DATABASE_URL`: Your external database connection string (e.g., `postgresql://user:password@host:port/dbname`)
7. Deploy the application

Vercel will automatically:
- Install dependencies from `requirements.txt`
- Run migrations and collect static files (via `vercel.json` buildCommand)

### Deploy to Render

Render provides a fully managed PostgreSQL database, making deployment straightforward.

#### Option 1: Using render.yaml (Recommended)

1. Fork this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file and set up:
   - A PostgreSQL database
   - A web service with the Django application
6. Set the required environment variables if not auto-generated:
   - `SECRET_KEY` (will be auto-generated)
   - `DEBUG` (set to `False` for production)

#### Option 2: Manual Setup

1. Create a new PostgreSQL database on Render
2. Create a new Web Service on Render
3. Configure the following:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn robotiki.wsgi:application`
   - **Environment Variables**:
     - `PYTHON_VERSION`: `3.11.0`
     - `SECRET_KEY`: (generate a secure secret key)
     - `DEBUG`: `False`
     - `DATABASE_URL`: (copy from your PostgreSQL database)

The application will automatically:
- Install dependencies from `requirements.txt`
- Run database migrations
- Collect static files

### Local Deployment

#### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

#### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/aloualou56/django_management.git
   cd django_management
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the root directory with:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```
   
   To generate a secure SECRET_KEY, you can use:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. Run database migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser (admin account):
   ```bash
   python manage.py createsuperuser
   ```

8. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

9. Run the development server:
   ```bash
   python manage.py runserver
   ```

10. Access the application at `http://127.0.0.1:8000/`

---

## Ελληνικά (Greek)

### Ανάπτυξη στο Vercel

**Σημαντικό:** Το Vercel απαιτεί εξωτερική βάση δεδομένων. Η SQLite δεν υποστηρίζεται σε παραγωγή στο Vercel. Πρέπει να χρησιμοποιήσετε μια εξωτερική υπηρεσία βάσης δεδομένων όπως:
- [Neon](https://neon.tech/) (PostgreSQL - Διαθέσιμο δωρεάν πλάνο)
- [PlanetScale](https://planetscale.com/) (MySQL - Διαθέσιμο δωρεάν πλάνο)
- [Supabase](https://supabase.com/) (PostgreSQL - Διαθέσιμο δωρεάν πλάνο)
- [Railway](https://railway.app/) (PostgreSQL)

#### Γρήγορη Ανάπτυξη

Κάντε κλικ παρακάτω για γρήγορη ανάπτυξη στο Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Faloualou56%2Fdjango_management)

#### Χειροκίνητη Εγκατάσταση

1. Κάντε fork αυτό το αποθετήριο στο λογαριασμό σας στο GitHub
2. Ρυθμίστε μια εξωτερική βάση δεδομένων PostgreSQL (π.χ., στο Neon, Supabase ή Railway)
3. Πηγαίνετε στο [Vercel Dashboard](https://vercel.com/dashboard)
4. Κάντε κλικ στο "Add New..." → "Project"
5. Εισάγετε το forked αποθετήριό σας
6. Ρυθμίστε τις μεταβλητές περιβάλλοντος:
   - `SECRET_KEY`: Δημιουργήστε ένα ασφαλές μυστικό κλειδί
   - `DEBUG`: Ορίστε σε `False`
   - `DATABASE_URL`: Η συμβολοσειρά σύνδεσης της εξωτερικής βάσης δεδομένων σας (π.χ., `postgresql://user:password@host:port/dbname`)
7. Αναπτύξτε την εφαρμογή

Το Vercel θα κάνει αυτόματα:
- Εγκατάσταση εξαρτήσεων από το `requirements.txt`
- Εκτέλεση migrations και συλλογή στατικών αρχείων (μέσω του `vercel.json` buildCommand)

### Ανάπτυξη στο Render

Το Render παρέχει πλήρως διαχειριζόμενη βάση δεδομένων PostgreSQL, καθιστώντας την ανάπτυξη απλή.

#### Επιλογή 1: Χρήση render.yaml (Συνιστάται)

1. Κάντε fork αυτό το αποθετήριο στο λογαριασμό σας στο GitHub
2. Πηγαίνετε στο [Render Dashboard](https://dashboard.render.com/)
3. Κάντε κλικ στο "New" → "Blueprint"
4. Συνδέστε το αποθετήριο σας στο GitHub
5. Το Render θα εντοπίσει αυτόματα το αρχείο `render.yaml` και θα ρυθμίσει:
   - Μια βάση δεδομένων PostgreSQL
   - Μια υπηρεσία web με την εφαρμογή Django
6. Ορίστε τις απαιτούμενες μεταβλητές περιβάλλοντος εάν δεν δημιουργηθούν αυτόματα:
   - `SECRET_KEY` (θα δημιουργηθεί αυτόματα)
   - `DEBUG` (ορίστε σε `False` για παραγωγή)

#### Επιλογή 2: Χειροκίνητη Εγκατάσταση

1. Δημιουργήστε μια νέα βάση δεδομένων PostgreSQL στο Render
2. Δημιουργήστε μια νέα υπηρεσία Web στο Render
3. Ρυθμίστε τα ακόλουθα:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn robotiki.wsgi:application`
   - **Μεταβλητές Περιβάλλοντος**:
     - `PYTHON_VERSION`: `3.11.0`
     - `SECRET_KEY`: (δημιουργήστε ένα ασφαλές μυστικό κλειδί)
     - `DEBUG`: `False`
     - `DATABASE_URL`: (αντιγράψτε από τη βάση δεδομένων PostgreSQL σας)

Η εφαρμογή θα κάνει αυτόματα:
- Εγκατάσταση εξαρτήσεων από το `requirements.txt`
- Εκτέλεση migrations βάσης δεδομένων
- Συλλογή στατικών αρχείων

### Τοπική Ανάπτυξη

#### Προαπαιτούμενα

- Python 3.11 ή νεότερη έκδοση
- pip (διαχειριστής πακέτων Python)
- Git

#### Βήματα Εγκατάστασης

1. Κλωνοποιήστε το αποθετήριο:
   ```bash
   git clone https://github.com/aloualou56/django_management.git
   cd django_management
   ```

2. Δημιουργήστε ένα εικονικό περιβάλλον:
   ```bash
   python -m venv venv
   ```

3. Ενεργοποιήστε το εικονικό περιβάλλον:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. Εγκαταστήστε τις εξαρτήσεις:
   ```bash
   pip install -r requirements.txt
   ```

5. Δημιουργήστε ένα αρχείο `.env` στον ριζικό κατάλογο με:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```
   
   Για να δημιουργήσετε ένα ασφαλές SECRET_KEY, μπορείτε να χρησιμοποιήσετε:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. Εκτελέστε τα migrations της βάσης δεδομένων:
   ```bash
   python manage.py migrate
   ```

7. Δημιουργήστε έναν superuser (λογαριασμό διαχειριστή):
   ```bash
   python manage.py createsuperuser
   ```

8. Συλλέξτε τα στατικά αρχεία:
   ```bash
   python manage.py collectstatic
   ```

9. Εκτελέστε τον διακομιστή ανάπτυξης:
   ```bash
   python manage.py runserver
   ```

10. Αποκτήστε πρόσβαση στην εφαρμογή στη διεύθυνση `http://127.0.0.1:8000/`
