from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from People.models import Student

class Month(models.Model):
    name = models.CharField(max_length=20, unique=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class PaymentPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    one_time_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    months = models.ManyToManyField(Month, related_name='payment_plans')

    def __str__(self):
        return self.name

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments', verbose_name=_("Student"), null=True)
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name='payments', verbose_name=_("Payment Plan"))
    one_time_fee_paid = models.BooleanField(default=False)
    months_paid = models.ManyToManyField(Month, blank=True, related_name='paid', verbose_name=_("Paid Months"))
    academic_year = models.CharField(max_length=9, verbose_name=_("Academic Year"), blank=True)

    def __str__(self):
        if self.student:
            return f'{_("Payment for")} {self.student} - {self.payment_plan}'
        return f'{_("Payment for")} Unknown Student - {self.payment_plan}'


    def save(self, *args, **kwargs):
        if not self.academic_year:
            current_year = timezone.now().year
            self.academic_year = f"{current_year}-{current_year + 1}"
        super().save(*args, **kwargs)

class Receipt(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='receipts', verbose_name=_("Payment"))
    receipt_number = models.CharField(max_length=100, verbose_name=_("Receipt Number"), unique=True)
    description = models.CharField(max_length=100, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount Paid"))

    def __str__(self):
        if self.payment.student:
            return f'{_("Receipt")} {self.receipt_number} {_("for")} {self.payment.student}'
        return f'{_("Receipt")} {self.receipt_number} {_("for")} Unknown Student'


@receiver(post_save, sender=Receipt)
def update_months_paid(sender, instance, created, **kwargs):
    if created:
        payment = instance.payment
        total_paid = sum(receipt.amount_paid for receipt in payment.receipts.all())
        payment_plan = payment.payment_plan
        
        # Calculate the amount paid towards monthly fees
        monthly_fee_paid = total_paid
        if payment_plan.one_time_fee > 0:
            if payment.one_time_fee_paid:
                monthly_fee_paid = total_paid - payment_plan.one_time_fee
            elif total_paid >= payment_plan.one_time_fee:
                payment.one_time_fee_paid = True
                monthly_fee_paid -= payment_plan.one_time_fee
            else:
                payment.save()
                return

        # Calculate the number of months paid
        months = payment.payment_plan.months.all()
        if payment_plan.monthly_fee > 0:
            months_to_pay = int(monthly_fee_paid // payment_plan.monthly_fee)
            payment.months_paid.set(months[:months_to_pay])
        payment.save()
