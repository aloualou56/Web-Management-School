from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import uuid
import random

class Student(models.Model):
    """
    Represents a student in the system.
    """
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message=_("Phone number must be exactly 10 digits.")
    )

    first_name = models.CharField(max_length=20, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=20, verbose_name=_("Last Name"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    phone_number = models.CharField(validators=[phone_validator], max_length=10, verbose_name=_("Phone Number"), blank=True)
    address = models.CharField(max_length=20, verbose_name=_("Address"))
    grade = models.ForeignKey('Class_related.Grade', on_delete=models.PROTECT, verbose_name=_("Grade"), blank=True, null=True)
    photo = models.ImageField(upload_to='images/', verbose_name=_("Photo"), blank=True)
    guardians = models.ManyToManyField('Guardian', related_name='students', blank=True, verbose_name=_("Guardians"))
    school = models.CharField(max_length=20, blank=True, verbose_name=_("School"))
    school_year = models.CharField(max_length=20, blank=True, verbose_name=_("School Year"))
    birth_date = models.DateField(verbose_name=_("Birth Date"), blank=True, null=True)
    payment_plan = models.ForeignKey('Payments.PaymentPlan', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Payment Plan"))
    presences = models.IntegerField(default=0, verbose_name=_("Presences"))
    absences = models.IntegerField(default=0, verbose_name=_("Absences"))
    email = models.EmailField(max_length=30, blank=True, verbose_name=_("Email"))
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_joined = models.DateField(default=timezone.now, verbose_name=_("Date Joined"))
    student_id = models.CharField(max_length=15, unique=True, blank=True, verbose_name=_("Student ID"))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def _generate_student_id(self):
        """Generate a unique student ID based on date joined and random numbers."""
        # Format: YYYYMMDD-RRRRR (e.g., 20231215-12345)
        date_part = self.date_joined.strftime('%Y%m%d')
        max_retries = 100  # Prevent infinite loop
        for _ in range(max_retries):
            random_part = str(random.randint(10000, 99999))
            student_id = f"{date_part}-{random_part}"
            if not Student.objects.filter(student_id=student_id).exists():
                return student_id
        # Fallback: use microseconds if all retries failed
        from django.utils import timezone
        microseconds = str(timezone.now().microsecond).zfill(6)[:5]
        return f"{date_part}-{microseconds}"

    def save(self, *args, **kwargs):
        # Generate student_id if not set
        if not self.student_id:
            self.student_id = self._generate_student_id()
        
        super().save(*args, **kwargs)
        if self.payment_plan and not self.payments.filter(payment_plan=self.payment_plan).exists():
            from Payments.models import Payment
            Payment.objects.create(
                student=self,
                payment_plan=self.payment_plan
            )

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

class Guardian(models.Model):
    """
    Represents a guardian of a student.
    """
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message=_("Phone number must be exactly 10 digits.")
    )

    first_name = models.CharField(max_length=20, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=20, verbose_name=_("Last Name"))
    phone_number = models.CharField(validators=[phone_validator], max_length=10, verbose_name=_("Phone Number"))
    address = models.CharField(max_length=20, verbose_name=_("Address"))
    landline_number = models.CharField(validators=[phone_validator], max_length=10, verbose_name=_("Landline Number"), blank=True)
    postal_code = models.CharField(max_length=5, blank=True, verbose_name=_("Postal Code"))
    profession = models.CharField(max_length=30, verbose_name=_("Profession"), blank=True)
    email = models.EmailField(max_length=30, blank=True, verbose_name=_("Email"))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('Guardian')
        verbose_name_plural = _('Guardians')
