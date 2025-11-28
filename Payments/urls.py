from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('plans/', views.payment_plan_list, name='payment_plan_list'),
    path('plans/create/', views.payment_plan_list, name='create_payment_plan'),
    path('plans/<int:payment_plan_id>/edit/', views.edit_payment_plan, name='edit_payment_plan'),
    path('plans/<int:payment_plan_id>/update/', views.update_payment_plan, name='update_payment_plan'),
    path('plans/<int:payment_plan_id>/delete/', views.delete_payment_plan, name='delete_payment_plan'),
    path('', views.payment_list, name='payment_list'),
    path('create/', views.add_payment, name='add_payment'),
    path('<int:payment_id>/delete/', views.delete_payment, name='delete_payment'),
    path('receipts/', views.receipt_list, name='receipt_list'),
    path('receipts/create/', views.add_receipt, name='add_receipt'),
]
