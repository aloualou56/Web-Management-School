from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Student, Guardian
from Class_related.models import Grade, Attendance
from Payments.models import PaymentPlan, Payment, Month
import json


class StudentUpdateTestCase(TestCase):
    """Test student update functionality including grade and payment plan changes"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create test data
        self.grade1 = Grade.objects.create(name='Grade 1', reset_time='10:00:00')
        self.grade2 = Grade.objects.create(name='Grade 2', reset_time='10:00:00')
        
        self.payment_plan1 = PaymentPlan.objects.create(
            name='Plan 1',
            one_time_fee=100.00,
            monthly_fee=50.00
        )
        self.payment_plan2 = PaymentPlan.objects.create(
            name='Plan 2',
            one_time_fee=200.00,
            monthly_fee=75.00
        )
        
        self.student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            address='123 Main St',
            grade=self.grade1,
            payment_plan=self.payment_plan1
        )
    
    def test_update_student_grade(self):
        """Test that updating a student's grade works correctly"""
        response = self.client.post(
            reverse('people:update_student', args=[self.student.id]),
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'address': '123 Main St',
                'phone_number': '',
                'email': '',
                'school': '',
                'school_year': '',
                'grade': self.grade2.id,
                'payment_plan': self.payment_plan1.id,
                'guardians': []
            }
        )
        
        self.student.refresh_from_db()
        self.assertEqual(self.student.grade, self.grade2)
    
    def test_update_student_payment_plan(self):
        """Test that updating a student's payment plan works correctly"""
        response = self.client.post(
            reverse('people:update_student', args=[self.student.id]),
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'address': '123 Main St',
                'phone_number': '',
                'email': '',
                'school': '',
                'school_year': '',
                'grade': self.grade1.id,
                'payment_plan': self.payment_plan2.id,
                'guardians': []
            }
        )
        
        self.student.refresh_from_db()
        self.assertEqual(self.student.payment_plan, self.payment_plan2)
    
    def test_remove_student_grade(self):
        """Test that removing a student's grade works correctly"""
        response = self.client.post(
            reverse('people:update_student', args=[self.student.id]),
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'address': '123 Main St',
                'phone_number': '',
                'email': '',
                'school': '',
                'school_year': '',
                'grade': '',
                'payment_plan': self.payment_plan1.id,
                'guardians': []
            }
        )
        
        self.student.refresh_from_db()
        self.assertIsNone(self.student.grade)


class PaymentPlanAssignmentTestCase(TestCase):
    """Test that creating a payment automatically assigns the payment plan to the student"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        self.payment_plan = PaymentPlan.objects.create(
            name='Test Plan',
            one_time_fee=100.00,
            monthly_fee=50.00
        )
        
        # Create student without payment plan
        self.student = Student.objects.create(
            first_name='Jane',
            last_name='Smith',
            address='456 Oak Ave'
        )
    
    def test_payment_assigns_plan_to_student(self):
        """Test that creating a payment assigns the payment plan to student if not already set"""
        response = self.client.post(
            reverse('payments:add_payment'),
            {
                'student': self.student.id,
                'payment_plan': self.payment_plan.id,
                'academic_year': '2024-2025'
            }
        )
        
        self.student.refresh_from_db()
        self.assertEqual(self.student.payment_plan, self.payment_plan)
    
    def test_payment_doesnt_override_existing_plan(self):
        """Test that creating a payment doesn't override existing payment plan"""
        # Set an initial payment plan
        other_plan = PaymentPlan.objects.create(
            name='Other Plan',
            one_time_fee=200.00,
            monthly_fee=75.00
        )
        self.student.payment_plan = other_plan
        self.student.save()
        
        response = self.client.post(
            reverse('payments:add_payment'),
            {
                'student': self.student.id,
                'payment_plan': self.payment_plan.id,
                'academic_year': '2024-2025'
            }
        )
        
        self.student.refresh_from_db()
        # Should keep the original plan
        self.assertEqual(self.student.payment_plan, other_plan)


class QRCodeGenerationTestCase(TestCase):
    """Test QR code generation for students"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        self.student = Student.objects.create(
            first_name='Test',
            last_name='Student',
            address='789 Pine Rd'
        )
    
    def test_qr_code_generation(self):
        """Test that QR code can be generated for a student"""
        response = self.client.get(
            reverse('people:student_qr_code', args=[self.student.id])
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertIn('qr_code', data)
        self.assertIn('student_name', data)
        self.assertIn('uuid', data)
        self.assertEqual(data['student_name'], 'Test Student')
        self.assertTrue(data['qr_code'].startswith('data:image/png;base64,'))


class AttendanceStatsTestCase(TestCase):
    """Test attendance statistics in attendance list view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        self.grade = Grade.objects.create(name='Test Grade', reset_time='10:00:00')
        
        # Create students with attendance records
        self.student1 = Student.objects.create(
            first_name='Student',
            last_name='One',
            address='111 Test St',
            grade=self.grade
        )
        self.student2 = Student.objects.create(
            first_name='Student',
            last_name='Two',
            address='222 Test St',
            grade=self.grade
        )
        
        # Create attendance records
        self.attendance1 = Attendance.objects.create(
            student=self.student1,
            grade=self.grade,
            present=True
        )
        self.attendance2 = Attendance.objects.create(
            student=self.student2,
            grade=self.grade,
            present=False
        )
    
    def test_attendance_list_shows_stats(self):
        """Test that attendance list view shows correct statistics"""
        response = self.client.get(reverse('class_related:attendance_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('grouped_attendances', response.context)
        
        # Check that stats are calculated correctly
        grade_data = response.context['grouped_attendances'][self.grade]
        self.assertEqual(grade_data['present_count'], 1)
        self.assertEqual(grade_data['absent_count'], 1)
        self.assertEqual(len(grade_data['attendances']), 2)

