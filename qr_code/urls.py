from django.urls import path
from .views import qr_result
from . import views

urlpatterns = [
    path('api/qr-result/', qr_result, name='qr_result'),
    path('generate-qr/<str:qrcodes>', views.generate_qr, name='generate_qr'),
    path('handle_scan/', views.handle_scan, name='handle_scan'),
]