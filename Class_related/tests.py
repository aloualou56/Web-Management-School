from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Grade, Attendance
from People.models import Student
import json
import os


class ServerTimeAPITestCase(TestCase):
    """Test the server time API endpoint"""
    
    def setUp(self):
        self.client = Client()
    
    def test_server_time_accessible_without_login(self):
        """Test that the server time API is accessible without login"""
        response = self.client.get(reverse('class_related:server_time'))
        self.assertEqual(response.status_code, 200)
    
    def test_server_time_returns_json(self):
        """Test that the server time API returns JSON"""
        response = self.client.get(reverse('class_related:server_time'))
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertIn('time', data)
        self.assertIn('weekday', data)
        self.assertIn('full_display', data)
    
    def test_server_time_format(self):
        """Test that the server time API returns correct format"""
        response = self.client.get(reverse('class_related:server_time'))
        data = json.loads(response.content)
        
        # Check time format (YYYY-MM-DD HH:MM:SS)
        time_str = data['time']
        self.assertRegex(time_str, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
        
        # Check weekday is present (3 letter abbreviation)
        weekday = data['weekday']
        self.assertIn(len(weekday), [3])
        
        # Check full_display contains UTC
        full_display = data['full_display']
        self.assertIn('UTC', full_display)


class AttendanceAPITestCase(TestCase):
    """Test the attendance automation API endpoints"""
    
    def setUp(self):
        self.client = Client()
        self.test_token = 'test-token-12345'
        
        # Set the token in the environment
        os.environ['ATTENDANCE_API_TOKEN'] = self.test_token
        
        # Create a test grade with active students
        self.grade = Grade.objects.create(
            name='Test Grade',
            reset_time='10:00:00',
            class_time='14:00:00',
            weekdays='MONDAY,WEDNESDAY,FRIDAY',
            lesson_duration=2
        )
        
        self.student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            address='123 Test St',
            grade=self.grade,
            active=True
        )
    
    def tearDown(self):
        # Clean up environment
        if 'ATTENDANCE_API_TOKEN' in os.environ:
            del os.environ['ATTENDANCE_API_TOKEN']
    
    def test_trigger_attendance_generation_unauthorized_no_token(self):
        """Test that endpoint returns 401 without authorization token"""
        response = self.client.post(
            reverse('class_related:trigger_attendance_generation')
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Unauthorized')
    
    def test_trigger_attendance_generation_unauthorized_wrong_token(self):
        """Test that endpoint returns 401 with wrong token"""
        response = self.client.post(
            reverse('class_related:trigger_attendance_generation'),
            HTTP_AUTHORIZATION='Bearer wrong-token'
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Unauthorized')
    
    def test_trigger_attendance_generation_missing_env_token(self):
        """Test that endpoint returns 500 when ATTENDANCE_API_TOKEN is not configured"""
        # Remove token from environment
        del os.environ['ATTENDANCE_API_TOKEN']
        
        response = self.client.post(
            reverse('class_related:trigger_attendance_generation'),
            HTTP_AUTHORIZATION='Bearer some-token'
        )
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertIn('ATTENDANCE_API_TOKEN not set', data['error'])
        
        # Restore token for other tests
        os.environ['ATTENDANCE_API_TOKEN'] = self.test_token
    
    def test_trigger_attendance_generation_success(self):
        """Test that endpoint successfully triggers attendance generation"""
        response = self.client.post(
            reverse('class_related:trigger_attendance_generation'),
            HTTP_AUTHORIZATION=f'Bearer {self.test_token}'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertIn('message', data)
    
    def test_trigger_attendance_autosave_unauthorized_no_token(self):
        """Test that autosave endpoint returns 401 without authorization token"""
        response = self.client.post(
            reverse('class_related:trigger_attendance_autosave')
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Unauthorized')
    
    def test_trigger_attendance_autosave_unauthorized_wrong_token(self):
        """Test that autosave endpoint returns 401 with wrong token"""
        response = self.client.post(
            reverse('class_related:trigger_attendance_autosave'),
            HTTP_AUTHORIZATION='Bearer wrong-token'
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Unauthorized')
    
    def test_trigger_attendance_autosave_success(self):
        """Test that autosave endpoint successfully triggers attendance autosave"""
        response = self.client.post(
            reverse('class_related:trigger_attendance_autosave'),
            HTTP_AUTHORIZATION=f'Bearer {self.test_token}'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertIn('message', data)
    
    def test_trigger_attendance_generation_only_post(self):
        """Test that attendance generation endpoint only accepts POST"""
        response = self.client.get(
            reverse('class_related:trigger_attendance_generation'),
            HTTP_AUTHORIZATION=f'Bearer {self.test_token}'
        )
        # Should return 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)
    
    def test_trigger_attendance_autosave_only_post(self):
        """Test that attendance autosave endpoint only accepts POST"""
        response = self.client.get(
            reverse('class_related:trigger_attendance_autosave'),
            HTTP_AUTHORIZATION=f'Bearer {self.test_token}'
        )
        # Should return 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)
    
    def test_trigger_attendance_generation_direct_api_url(self):
        """Test that attendance generation is accessible via direct /api/ URL"""
        response = self.client.post(
            '/api/trigger-attendance-generation/',
            HTTP_AUTHORIZATION=f'Bearer {self.test_token}'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
    
    def test_trigger_attendance_autosave_direct_api_url(self):
        """Test that attendance autosave is accessible via direct /api/ URL"""
        response = self.client.post(
            '/api/trigger-attendance-autosave/',
            HTTP_AUTHORIZATION=f'Bearer {self.test_token}'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')


class DeleteGradeTestCase(TestCase):
    """Test deleting a grade with students assigned to it"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create test grade
        self.grade = Grade.objects.create(name='Test Grade', reset_time='10:00:00')
        
        # Create students assigned to the grade
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
        # Create a student not assigned to the grade
        self.student3 = Student.objects.create(
            first_name='Student',
            last_name='Three',
            address='333 Test St',
            grade=None
        )
    
    def test_delete_grade_with_students(self):
        """Test that deleting a grade unassigns students and deletes the grade"""
        # Verify students are assigned to the grade
        self.assertEqual(Student.objects.filter(grade=self.grade).count(), 2)
        
        # Delete the grade
        response = self.client.post(
            reverse('class_related:delete_grade', args=[self.grade.id])
        )
        
        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('class_related:grade_list'))
        
        # Verify grade was deleted
        self.assertFalse(Grade.objects.filter(id=self.grade.id).exists())
        
        # Verify students were unassigned (grade set to None)
        self.student1.refresh_from_db()
        self.student2.refresh_from_db()
        self.assertIsNone(self.student1.grade)
        self.assertIsNone(self.student2.grade)
        
        # Verify all students still exist
        self.assertTrue(Student.objects.filter(id=self.student1.id).exists())
        self.assertTrue(Student.objects.filter(id=self.student2.id).exists())
        self.assertTrue(Student.objects.filter(id=self.student3.id).exists())
    
    def test_delete_grade_without_students(self):
        """Test that deleting a grade without students works correctly"""
        # Create grade without students
        empty_grade = Grade.objects.create(name='Empty Grade', reset_time='11:00:00')
        
        # Delete the grade
        response = self.client.post(
            reverse('class_related:delete_grade', args=[empty_grade.id])
        )
        
        # Check redirect
        self.assertEqual(response.status_code, 302)
        
        # Verify grade was deleted
        self.assertFalse(Grade.objects.filter(id=empty_grade.id).exists())


