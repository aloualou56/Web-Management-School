from django.contrib import admin
from .models import Student, Guardian
from django.utils.translation import gettext_lazy as _

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    filter_horizontal = ('guardians',)
    list_display = ('student_id', 'first_name', 'last_name', 'active', 'phone_number', 'address', 'grade', 'school', 'date_joined')
    search_fields = ('student_id', 'first_name', 'last_name', 'phone_number', 'school', 'school_year', 'email')
    autocomplete_fields = ['payment_plan']
    readonly_fields = ('student_id', 'uuid', 'date_joined')
    list_filter = ('active', 'grade', 'date_joined')

    def guardian_list(self, obj):
        return ", ".join([str(guardian) for guardian in obj.guardians.all()])
    guardian_list.short_description = _('Guardians')

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'landline_number', 'address', 'profession', 'postal_code', 'email')
    search_fields = ('first_name', 'last_name', 'phone_number', 'profession', 'postal_code', 'email')
