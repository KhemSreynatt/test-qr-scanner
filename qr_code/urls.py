from django.urls import path
from . import views
from rest_framework import routers
from .views import  NetworkInfoCreateView, AttendanceCreateView
router= routers.DefaultRouter()
router.register(r'qr_code',views.NetworkInfoCreateView)

urlpatterns = [
    path('api/generate_qrcode/', views.generate_qrcode, name='generate_qr_code'),
    path('api/wifi_scanner', views.generate_qr_scanner,name='wifi_scanner'),
    path('api/qr-result/', views.qr_result, name='qr_result'),
    path('generate-qr/<str:qrcodes>', views.generate_qr, name='generate_qr'),
    # network
    path('api/network-info/get', NetworkInfoCreateView.as_view(), name='get_network_info'),
    path('api/network-info/post', views.post_NetworkInfo,name='post_NetworkInfo'),
    path('api/network-info/update/<int:id>', views.update_network_gps,name='update_network_info'),
    path('api/network-info/delete/<str:id>/', views.delete_NetworkInfo, name='delete_NetworkInfo'),
    # attendance
    path('api/attendance/get', AttendanceCreateView.as_view(), name='get_attendance'),
    path('api/attendance/post', views.post_Attendance,name='post_Attendance'),
    path('api/attendance/update/<int:id>', views.update_attendance,name='update_attendance'),
    path('api/attendace/user/<str:tg_id>',views.get_attendance_by_user, name='get_attendance_by_user'),
    path('api/attendance/delete/<int:id>/', views.delete_attendance_by_user, name='delete_attendance_by_user'),
    
]