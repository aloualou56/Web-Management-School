from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from .models import PaymentPlan, Payment, Receipt, Month
from People.models import Student

@login_required
def payment_plan_list(request):
    payment_plans = PaymentPlan.objects.all()
    months = Month.objects.all()

    if request.method == "POST":
        form_data = request.POST
        name = form_data.get('name')
        description = form_data.get('description')
        one_time_fee = form_data.get('one_time_fee')
        monthly_fee = form_data.get('monthly_fee')
        months_ids = form_data.getlist('months')
        selected_months = Month.objects.filter(id__in=months_ids)

        payment_plan = PaymentPlan.objects.create(
            name=name,
            description=description,
            one_time_fee=one_time_fee,
            monthly_fee=monthly_fee
        )
        payment_plan.months.set(selected_months)
        return redirect('payments:payment_plan_list')

    context = {
        'payment_plans': payment_plans,
        'months': months
    }
    return render(request, 'payment_plans.html', context)

@login_required
def payment_list(request):
    payments = Payment.objects.all()
    for payment in payments:
        payment.total_amount_paid = sum(receipt.amount_paid for receipt in payment.receipts.all())

    context = {
        'payments': payments
    }
    return render(request, 'payments.html', context)

@login_required
def add_payment(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        payment_plan_id = request.POST.get('payment_plan')
        academic_year = request.POST.get('academic_year')

        try:
            student = get_object_or_404(Student, id=student_id)
            payment_plan = get_object_or_404(PaymentPlan, id=payment_plan_id)
            
            # Update student's payment plan if not already set
            if not student.payment_plan:
                student.payment_plan = payment_plan
                student.save()
            
            Payment.objects.create(
                student=student,
                payment_plan=payment_plan,
                academic_year=academic_year
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': _('Invalid request')}, status=400)

@login_required
def edit_payment_plan(request, payment_plan_id):
    payment_plan = get_object_or_404(PaymentPlan, id=payment_plan_id)
    data = {
        'id': payment_plan.id,
        'name': payment_plan.name,
        'description': payment_plan.description,
        'one_time_fee': payment_plan.one_time_fee,
        'monthly_fee': payment_plan.monthly_fee,
        'months': [m.id for m in payment_plan.months.all()]
    }
    return JsonResponse(data)

@login_required
def update_payment_plan(request, payment_plan_id):
    if request.method == 'POST':
        payment_plan = get_object_or_404(PaymentPlan, id=payment_plan_id)
        payment_plan.name = request.POST.get('name')
        payment_plan.description = request.POST.get('description')
        payment_plan.one_time_fee = request.POST.get('one_time_fee')
        payment_plan.monthly_fee = request.POST.get('monthly_fee')
        payment_plan.save()
        months_ids = request.POST.getlist('months')
        selected_months = Month.objects.filter(id__in=months_ids)
        payment_plan.months.set(selected_months)
    return redirect('payments:payment_plan_list')

@login_required
def delete_payment_plan(request, payment_plan_id):
    if request.method == 'POST':
        payment_plan = get_object_or_404(PaymentPlan, id=payment_plan_id)
        payment_plan.delete()
    return redirect('payments:payment_plan_list')

@login_required
def delete_payment(request, payment_id):
    if request.method == 'POST':
        payment = get_object_or_404(Payment, id=payment_id)
        payment.delete()
    return redirect('payments:payment_list')

@login_required
def add_receipt(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        receipt_number = request.POST.get('receipt_number')
        description = request.POST.get('description')
        amount_paid = request.POST.get('amount_paid')
        payment = get_object_or_404(Payment, id=payment_id)
        Receipt.objects.create(
            payment=payment,
            receipt_number=receipt_number,
            description=description,
            amount_paid=amount_paid
        )
    return redirect('payments:payment_list')

@login_required
def receipt_list(request):
    receipts = Receipt.objects.all()
    context = {
        "receipts": receipts
    }
    return render(request, 'receipts.html', context)
