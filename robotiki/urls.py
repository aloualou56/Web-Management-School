"""
URL configuration for robotiki project.
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from People.views import index
from Class_related import views as class_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payments/', include('Payments.urls', namespace='payments')),
    path('people/', include('People.urls', namespace='people')),
    path('class/', include('Class_related.urls', namespace='class_related')),
    # Direct API endpoints for external access (e.g., GitHub Actions)
    path('api/trigger-attendance-generation/', class_views.trigger_attendance_generation, name='api_trigger_attendance_generation'),
    path('api/trigger-attendance-autosave/', class_views.trigger_attendance_autosave, name='api_trigger_attendance_autosave'),
    path('', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
