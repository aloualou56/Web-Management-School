from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from datetime import datetime
from .models import Student, Guardian
from Class_related.models import Grade, Attendance
from Payments.models import PaymentPlan
import qrcode
from io import BytesIO
import base64


def login(request):
    """
    Custom login view with custom template.
    """
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        next_url = request.POST.get('next') or request.GET.get('next') or 'index'
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            # Handle "remember me" functionality
            if not remember:
                request.session.set_expiry(0)  # Session expires when browser closes
            
            return redirect(next_url)
        else:
            context = {
                'error_message': 'Invalid username or password. Please try again.',
                'username': username,
                'next': next_url,
            }
            return render(request, 'login.html', context)
    
    next_url = request.GET.get('next', 'index')
    return render(request, 'login.html', {'next': next_url})


def logout(request):
    """
    Custom logout view.
    """
    auth_logout(request)
    return redirect('people:login')

@login_required
def student_list(request):
    """
    Display a list of students and handle the creation of new students.
    """
    search_query = request.GET.get('search', '')
    if search_query:
        students = Student.objects.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(phone_number__icontains=search_query)
        )
    else:
        students = Student.objects.all()

    grades = Grade.objects.all()
    payment_plans = PaymentPlan.objects.all()
    guardians = Guardian.objects.all()

    if request.method == "POST":
        form_data = request.POST
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        phone_number = form_data.get('phone_number')
        address = form_data.get('address')
        grade_id = form_data.get('grade')
        grade = get_object_or_404(Grade, id=grade_id) if grade_id else None
        photo = request.FILES.get('photo')
        payment_plan_id = form_data.get('payment_plan')
        payment_plan = get_object_or_404(PaymentPlan, id=payment_plan_id) if payment_plan_id else None
        guardian_ids = form_data.getlist('guardians')
        selected_guardians = Guardian.objects.filter(id__in=guardian_ids)
        
        # Parse birth_date from DD/MM/YYYY format
        birth_date = form_data.get('birth_date')
        if birth_date:
            try:
                birth_date = datetime.strptime(birth_date, '%d/%m/%Y').date()
            except ValueError:
                birth_date = None
        else:
            birth_date = None

        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            grade=grade,
            photo=photo,
            payment_plan=payment_plan,
            birth_date=birth_date,
            email=form_data.get('email', ''),
            school=form_data.get('school', ''),
            school_year=form_data.get('school_year', '')
        )
        student.guardians.set(selected_guardians)
        return redirect('people:student_list')

    context = {
        'students': students,
        'grades': grades,
        'payment_plans': payment_plans,
        'guardians': guardians
    }
    return render(request, 'students.html', context)

@login_required
def create_student(request):
    # This view is merged into student_list, but can be separated if needed
    return redirect('people:student_list')

@login_required
def student_detail(request, student_id):
    """
    Display detailed information about a specific student.
    """
    student = get_object_or_404(Student, id=student_id)
    grades = Grade.objects.all()
    payment_plans = PaymentPlan.objects.all()
    guardians = Guardian.objects.all()
    
    context = {
        'student': student,
        'grades': grades,
        'payment_plans': payment_plans,
        'guardians': guardians
    }
    return render(request, 'student_detail.html', context)

@login_required
def edit_student(request, student_id):
    """
    Handle editing of an existing student.
    """
    student = get_object_or_404(Student, id=student_id)
    
    # Format birth_date as DD/MM/YYYY if it exists
    birth_date_formatted = student.birth_date.strftime('%d/%m/%Y') if student.birth_date else ''
    
    data = {
        'id': student.id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'phone_number': student.phone_number,
        'address': student.address,
        'school': student.school,
        'school_year': student.school_year,
        'birth_date': birth_date_formatted,
        'email': student.email,
        'grade': {'id': student.grade.id} if student.grade else None,
        'payment_plan': {'id': student.payment_plan.id} if student.payment_plan else None,
        'guardian_ids': [g.id for g in student.guardians.all()]
    }
    return JsonResponse(data)

@login_required
def update_student(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.phone_number = request.POST.get('phone_number')
        student.address = request.POST.get('address')
        student.school = request.POST.get('school')
        student.school_year = request.POST.get('school_year')
        
        # Handle birth_date - parse from DD/MM/YYYY format
        birth_date = request.POST.get('birth_date')
        if birth_date:
            try:
                student.birth_date = datetime.strptime(birth_date, '%d/%m/%Y').date()
            except ValueError:
                student.birth_date = None
        else:
            student.birth_date = None
        
        student.email = request.POST.get('email')
        
        # Update grade
        grade_id = request.POST.get('grade')
        if grade_id:
            student.grade = get_object_or_404(Grade, id=grade_id)
        else:
            student.grade = None
        
        # Update payment plan
        payment_plan_id = request.POST.get('payment_plan')
        if payment_plan_id:
            student.payment_plan = get_object_or_404(PaymentPlan, id=payment_plan_id)
        else:
            student.payment_plan = None
        
        student.save()
        guardian_ids = request.POST.getlist('guardians')
        selected_guardians = Guardian.objects.filter(id__in=guardian_ids)
        student.guardians.set(selected_guardians)
    return redirect('people:student_list')

@login_required
def delete_student(request, student_id):
    """
    Handle deletion of a student.
    """
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        student.delete()
    return redirect('people:student_list')

@login_required
def guardian_list(request):
    """
    Display a list of guardians and handle the creation of new guardians.
    """
    search_query = request.GET.get('search', '')
    if search_query:
        guardians = Guardian.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(profession__icontains=search_query)
        )
    else:
        guardians = Guardian.objects.all()
    
    students = Student.objects.all()

    if request.method == "POST":
        form_data = request.POST
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        phone_number = form_data.get('phone_number')
        landline_number = form_data.get('landline_number')
        address = form_data.get('address')
        postal_code = form_data.get('postal_code')
        profession = form_data.get('profession')
        email = form_data.get('email')
        student_ids = form_data.getlist('students')
        selected_students = Student.objects.filter(id__in=student_ids)

        guardian = Guardian.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            landline_number=landline_number,
            address=address,
            postal_code=postal_code,
            profession=profession,
            email=email
        )
        guardian.students.set(selected_students)
        return redirect('people:guardian_list')

    context = {
        'guardians': guardians,
        'students': students
    }
    return render(request, 'guardians.html', context)

@login_required
def create_guardian(request):
    # This view is merged into guardian_list, but can be separated if needed
    return redirect('people:guardian_list')

@login_required
def edit_guardian(request, guardian_id):
    """
    Handle editing of an existing guardian.
    """
    guardian = get_object_or_404(Guardian, id=guardian_id)
    data = {
        'id': guardian.id,
        'first_name': guardian.first_name,
        'last_name': guardian.last_name,
        'phone_number': guardian.phone_number,
        'landline_number': guardian.landline_number,
        'address': guardian.address,
        'postal_code': guardian.postal_code,
        'profession': guardian.profession,
        'email': guardian.email,
        'student_ids': [s.id for s in guardian.students.all()]
    }
    return JsonResponse(data)

@login_required
def update_guardian(request, guardian_id):
    if request.method == 'POST':
        guardian = get_object_or_404(Guardian, id=guardian_id)
        guardian.first_name = request.POST.get('first_name')
        guardian.last_name = request.POST.get('last_name')
        guardian.phone_number = request.POST.get('phone_number')
        guardian.landline_number = request.POST.get('landline_number')
        guardian.address = request.POST.get('address')
        guardian.postal_code = request.POST.get('postal_code')
        guardian.profession = request.POST.get('profession')
        guardian.email = request.POST.get('email')
        guardian.save()
        student_ids = request.POST.getlist('students')
        selected_students = Student.objects.filter(id__in=student_ids)
        guardian.students.set(selected_students)
    return redirect('people:guardian_list')

@login_required
def delete_guardian(request, guardian_id):
    """
    Handle deletion of a guardian.
    """
    if request.method == 'POST':
        guardian = get_object_or_404(Guardian, id=guardian_id)
        guardian.delete()
    return redirect('people:guardian_list')

@login_required
def barcode_scanner(request):
    """
    Render the barcode scanner page.
    """
    return render(request, 'scanner.html')

def index(request):
    """
    Display the main index page with counts of students, grades, and payment plans.
    """
    student_count = Student.objects.count()
    grade_count = Grade.objects.count()
    payment_plan_count = PaymentPlan.objects.count()

    context = {
        'student_count': student_count,
        'grade_count': grade_count,
        'payment_plan_count': payment_plan_count,
    }
    return render(request, 'index.html', context)

@login_required
def check_attendance(request):
    """
    Check student attendance based on a provided text input.
    """
    if request.method == "POST":
        input_text = request.POST.get('text_input', '')
        try:
            student = Student.objects.get(uuid=input_text)
            attendance, created = Attendance.objects.get_or_create(student=student)
            attendance.present = True
            attendance.save()
            return JsonResponse({'match': True, 'message': _('Attendance marked as present.')})
        except Student.DoesNotExist:
            return JsonResponse({'match': False, 'message': _('No match found.')})
    return JsonResponse({'error': _('Invalid request method.')})

@login_required
def student_qr_code(request, student_id):
    """
    Generate and return QR code for a student.
    """
    student = get_object_or_404(Student, id=student_id)
    
    # Create QR code with student's UUID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(student.uuid))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return JsonResponse({
        'qr_code': f'data:image/png;base64,{img_str}',
        'student_name': f'{student.first_name} {student.last_name}',
        'student_id': student.id,
        'uuid': str(student.uuid)
    })

@login_required
def generate_all_qr_codes(request):
    """
    View to display QR codes for all students.
    """
    students = Student.objects.filter(active=True).order_by('last_name', 'first_name')
    return render(request, 'qr_codes.html', {'students': students})
