from django.test import TestCase
from .models import Month


class MonthModelTest(TestCase):
    """Test the Month model and data migration."""
    
    def test_months_populated(self):
        """Test that all 12 months are populated in the database."""
        # The migration should have created 12 months
        self.assertEqual(Month.objects.count(), 12)
    
    def test_months_have_correct_order(self):
        """Test that months are ordered correctly."""
        months = Month.objects.all().order_by('order')
        expected_months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        
        for i, month in enumerate(months, start=1):
            self.assertEqual(month.order, i)
            self.assertEqual(month.name, expected_months[i-1])
    
    def test_month_names_unique(self):
        """Test that month names are unique."""
        month_names = Month.objects.values_list('name', flat=True)
        self.assertEqual(len(month_names), len(set(month_names)))
    
    def test_month_string_representation(self):
        """Test the string representation of Month."""
        january = Month.objects.get(name='January')
        self.assertEqual(str(january), 'January')
