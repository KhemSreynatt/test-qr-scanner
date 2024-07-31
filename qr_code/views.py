
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
from PIL import Image, ImageDraw, ImageFont
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


@api_view(['POST'])
def generate_qr_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_keys = ["ssid", "dssid", "ip", "gps", "branch", "branch_id"]
            if not all(key in data for key in required_keys):
                return JsonResponse({'error': 'Missing required keys'}, status=400)

            data_string = json.dumps(data)

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data_string)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white').convert('RGB')

            branch = data.get('branch', 'Unknown Branch')
            text = f"Office: {branch}"
            draw = ImageDraw.Draw(img)
           # Load custom font
            font_path = "font/arialbd.ttf"  # Update this path to your font file
            font_size = 24
            font = ImageFont.truetype(font_path, font_size)

            # Calculate text size using textbbox
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            img_width, img_height = img.size

            # Create a new image with extra space for the text
            new_img_height = img_height + text_height + 30
            new_img = Image.new('RGB', (img_width, new_img_height), 'white')
            new_img.paste(img, (0, 0))

            draw = ImageDraw.Draw(new_img)
            text_position = ((img_width - text_width) // 2, img_height )
            draw.text(text_position, text, fill='black', font=font)

            response = HttpResponse(content_type="image/png")
            new_img.save(response, "PNG")
            return response
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)