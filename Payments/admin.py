from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import PaymentPlan, Month, Payment, Receipt

class ReceiptInline(admin.TabularInline):
    model = Receipt
    extra = 1

class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'one_time_fee', 'monthly_fee')
    search_fields = ('name',)
    filter_horizontal = ('months',)

    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        (_('Pricing'), {
            'fields': ('one_time_fee', 'monthly_fee')
        }),
        (_('Months'), {
            'fields': ('months',)
        }),
    )

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'payment_plan' in self.data:
            try:
                payment_plan_id = int(self.data.get('payment_plan'))
                self.fields['months_paid'].queryset = Month.objects.filter(payment_plans__id=payment_plan_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['months_paid'].queryset = self.instance.payment_plan.months.all()

class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    inlines = [ReceiptInline]

    def display_months_paid(self, obj):
        return ", ".join([month.name for month in obj.months_paid.all()])
    display_months_paid.short_description = _('Paid Months')

    def total_amount_paid(self, obj):
        return sum(receipt.amount_paid for receipt in obj.receipts.all())
    total_amount_paid.short_description = _('Total Amount Paid')

    def display_months_unpaid(self, obj):
        months_from_plan = set(obj.payment_plan.months.values_list('id', flat=True))
        months_paid_ids = set(obj.months_paid.values_list('id', flat=True))
        unpaid_months_ids = months_from_plan - months_paid_ids
        unpaid_months = Month.objects.filter(id__in=unpaid_months_ids)
        return ", ".join([month.name for month in unpaid_months])
    display_months_unpaid.short_description = _('Unpaid Months')

    list_display = ('student', 'payment_plan', 'academic_year', 'one_time_fee_paid', 'display_months_paid', 'display_months_unpaid', 'total_amount_paid')
    search_fields = ('student__first_name', 'student__last_name', 'payment_plan__name')
    autocomplete_fields = ['student', 'payment_plan']
    readonly_fields = ('display_months_paid', 'display_months_unpaid')

    fieldsets = (
        (None, {
            'fields': ('student', 'payment_plan', 'one_time_fee_paid')
        }),
        (_('Months Management'), {
            'fields': ('months_paid',),
        }),
    )

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentPlan, PaymentPlanAdmin)
admin.site.register(Month)
