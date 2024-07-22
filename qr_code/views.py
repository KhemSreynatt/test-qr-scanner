
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

# Network and GPS
class NetworkGPSCreateView(ListAPIView):
    queryset = NetworkGPS.objects.all()
    serializer_class= NetworkGPSSerailizer

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
 

