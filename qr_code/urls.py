from django.urls import path
from .views import qr_result
from . import views

urlpatterns = [
    path('api/qr-result/', qr_result, name='qr_result'),
    path('generate-qr/<str:employee_id>/', views.generate_qr, name='generate_qr'),
    path('api/process-attendance/', views.process_attendance, name='process_attendance'),
    # path('scanner/', views.scanner_page, name='scanner_page'),
]