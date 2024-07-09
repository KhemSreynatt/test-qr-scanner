from django.urls import path
from .views import qr_result

urlpatterns = [
    path('api/qr-result/', qr_result, name='qr_result'),
]