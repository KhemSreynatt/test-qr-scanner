from django.urls import path
from .views import qr_result
from . import views
from rest_framework import routers
from .views import NetworkGPSCreateView, AttendanceCreateView
router= routers.DefaultRouter()
router.register(r'qr_code',views.NetworkGPSCreateView)

urlpatterns = [
    path('api/qr-result/', qr_result, name='qr_result'),
    path('generate-qr/<str:qrcodes>', views.generate_qr, name='generate_qr'),
    # network
    path('api/network-gps/get', NetworkGPSCreateView.as_view(), name='get_network-gps'),
    path('api/network-gps/post', views.post_networkGps,name='post_networkGps'),
    path('api/network-gps/update/<int:id>', views.update_network_gps,name='update_network_gps'),
    path('api/network-gps/delete/<str:id>/', views.delete_networkGps, name='delete_networkGps'),
    # attendance
    path('api/attendance/get', AttendanceCreateView.as_view(), name='get_network-gps'),
    path('api/attendance/post', views.post_Attendance,name='post_Attendance'),
    path('api/attendance/update/<int:id>', views.update_attendance,name='update_attendance'),
    path('api/attendace/user/<str:tg_id>',views.get_attendance_by_user, name='get_attendance_by_user'),
    path('api/attendance/delete/<int:id>/', views.delete_attendance_by_user, name='delete_attendance_by_user'),
    
]