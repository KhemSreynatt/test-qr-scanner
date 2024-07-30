
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import qrcode
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils import timezone
from io import BytesIO
from rest_framework import status
from .serializers import NetworkGPSSerailizer, AttendanceSerailizer
from .models import NetworkGPS, Attendances
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
import io
# Network and GPS
class NetworkGPSCreateView(ListAPIView):
    queryset = NetworkGPS.objects.all()
    serializer_class= NetworkGPSSerailizer
# dfdf
@api_view(['POST'])
def post_networkGps(request):
    if request.method=="POST":
        serializer = NetworkGPSSerailizer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'PATCH'])
def update_network_gps(request, id):
    try:
        networkgps = NetworkGPS.objects.get(id=id)
    except NetworkGPS.DoesNotExist:
        return Response({'error': 'Network IP and GPS not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = NetworkGPSSerailizer(networkgps, data=request.data)
    elif request.method == 'PATCH':
        serializer = NetworkGPSSerailizer(networkgps, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_networkGps(request, id):
    try:
     
        attendances = NetworkGPS.objects.filter(id=id)
        if not attendances.exists():
            return Response({"detail": "No attendance records found for this user."}, status=status.HTTP_404_NOT_FOUND)
        attendances.delete()
        return Response({"detail": "Attendance records deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Attendance Record
class AttendanceCreateView(ListAPIView):
    queryset = Attendances.objects.all()
    serializer_class= AttendanceSerailizer

@api_view(['POST'])
def post_Attendance(request):
    if request.method=="POST":
        serializer = AttendanceSerailizer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'PATCH'])
def update_attendance(request, id):
    tg_id= request.data.get("tg_id",'')
    try:
        attendendance = Attendances.objects.get(id=id,tg_id=tg_id)
    except Attendances.DoesNotExist:
        return Response({'error': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = AttendanceSerailizer(attendendance, data=request.data)
    elif request.method == 'PATCH':
        serializer = AttendanceSerailizer(attendendance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_attendance_by_user(request, tg_id):
    try:
        # Filter attendances by employee_id
        attendances = Attendances.objects.filter(tg_id=tg_id)
        if not attendances.exists():
            return Response({"detail": "No attendance records found for this user."}, status=status.HTTP_404_NOT_FOUND)
        # Serialize the data
        serializer = AttendanceSerailizer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_attendance_by_user(request, id):
    try:
        # Filter attendances by employee_id
        attendances = Attendances.objects.filter(id=id)
        if not attendances.exists():
            return Response({"detail": "No attendance records found for this user."}, status=status.HTTP_404_NOT_FOUND)
        # Delete the records
        attendances.delete()
        return Response({"detail": "Attendance records deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# qr code
@api_view(['POST'])
def qr_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = data.get('result')
        return JsonResponse({'status': 'success', 'message': f'Processed QR: {result}'})
    return JsonResponse({'status': 'error'}, status=400)


def generate_qr(request, qrcodes):
    event_id = f"{qrcodes}_{timezone.now().strftime('%Y%m%d%H%M%S')}"
    qr_data = json.dumps({
        "qrcodes": qrcodes,
    })
    img = qrcode.make(qrcodes)
    response = HttpResponse(content_type="image/png")
    buffer = BytesIO()
    img.save(buffer, "PNG")
    response.write(buffer.getvalue())
    return response


#  GENERATE QR CODE 
@api_view(['POST'])
def generate_qr_scanner(request):
    try:
        data = json.loads(request.body)
        ssid = data.get('ssid')
        password = data.get('password')

        if not ssid or not password:
            return HttpResponse('SSID and password are required', status=400)

        qr_data = f"WIFI:S:{ssid};T:WPA;P:{password};;"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)

        return HttpResponse(buf, content_type="image/png")

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


from django.http import JsonResponse
import psutil
import subprocess
import re
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_wifi_info(request):
    wifi_info = {}
    
    # Get SSID and BSSID
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode("utf-8")
        ssid = re.search("SSID\s+:\s(.*)", result)
        if ssid:
            wifi_info['ssid'] = ssid.group(1)
        bssid = re.search("BSSID\s+:\s(.*)", result)
        if bssid:
            wifi_info['bssid'] = bssid.group(1)
    except:
        wifi_info['ssid'] = "Not available"
        wifi_info['bssid'] = "Not available"
    
    # Get IP address
    try:
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == 2:  # AF_INET (IPv4)
                    wifi_info['ip'] = addr.address
                    break
            if 'ip' in wifi_info:
                break
    except:
        wifi_info['ip'] = "Not available"
    
    # Get MAC address
    try:
        wifi_info['mac'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    except:
        wifi_info['mac'] = "Not available"
    
    return Response(wifi_info)

    # ======

import psutil
import uuid
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from winwifi import WinWiFi

@api_view(['GET'])
def get_wifi(request):
    wifi_info = {}
    
    # Get SSID, BSSID, and other WiFi information
    try:
        current_connections = WinWiFi.get_connected_interfaces()
        if current_connections:
            current_connection = current_connections[0]  # Assume the first connected interface
            wifi_info['ssid'] = current_connection.ssid
            wifi_info['bssid'] = current_connection.bssid
            wifi_info['wifi_name'] = current_connection.ssid  # WiFi name is typically the same as SSID
            wifi_info['signal_strength'] = current_connection.signal
    except Exception as e:
        wifi_info['ssid'] = "Not available"
        wifi_info['bssid'] = "Not available"
        wifi_info['wifi_name'] = "Not available"
        wifi_info['signal_strength'] = "Not available"
        print(f"Error getting WiFi info: {str(e)}")
    
    # Get IP address
    try:
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == 2:  # AF_INET (IPv4)
                    wifi_info['ip'] = addr.address
                    break
            if 'ip' in wifi_info:
                break
    except Exception as e:
        wifi_info['ip'] = "Not available"
        print(f"Error getting IP address: {str(e)}")
    
    # Get MAC address
    try:
        wifi_info['mac'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    except Exception as e:
        wifi_info['mac'] = "Not available"
        print(f"Error getting MAC address: {str(e)}")
    
    return Response(wifi_info)



#    -----

import json
import subprocess
import platform

@api_view(['GET'])
def wifi_info(request):
    wifi_info = {}

    if platform.system() == "Windows":
        try:
            # Use 'netsh wlan show interfaces' to get WiFi information
            netsh_output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8')
            for line in netsh_output.split('\n'):
                if 'SSID' in line and 'BSSID' not in line:
                    wifi_info['ssid'] = line.split(':')[1].strip()
                elif 'BSSID' in line:
                    wifi_info['bssid'] = line.split(':')[1].strip()
                elif 'Physical address' in line:
                    wifi_info['mac_address'] = line.split(':')[1].strip()
            
            # Use 'ipconfig' to get the IP address
            ipconfig_output = subprocess.check_output(['ipconfig']).decode('utf-8')
            for line in ipconfig_output.split('\n'):
                if 'IPv4 Address' in line:
                    wifi_info['ip_address'] = line.split(':')[1].strip()

            # Assuming the WiFi name is the same as SSID
            wifi_info['wifi_name'] = wifi_info.get('ssid', 'Unknown')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Unsupported platform'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(wifi_info, status=status.HTTP_200_OK)




