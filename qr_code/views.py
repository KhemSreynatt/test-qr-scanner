
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def qr_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = data.get('result')
        # Process the result as needed
        return JsonResponse({'status': 'success', 'message': f'Processed QR: {result}'})
    return JsonResponse({'status': 'error'}, status=400)


#  Generate QR 

# views.py
import qrcode
from django.http import HttpResponse
from django.utils import timezone
import json
from io import BytesIO


def generate_qr(request, employee_id):
    # Create a unique identifier for this check-in/out event
    event_id = f"{employee_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create QR code data
    qr_data = json.dumps({
        # "event_id": event_id,
        "employee_id": employee_id,
        # "timestamp": timezone.now().isoformat()
    })
    
    # Generate QR code
    img = qrcode.make(employee_id)
    
    # Create a response
    response = HttpResponse(content_type="image/png")
    buffer = BytesIO()
    img.save(buffer, "PNG")
    response.write(buffer.getvalue())
    return response

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from geopy.geocoders import Nominatim
from bot import send_to_telegram_group  # You'll need to implement this

@csrf_exempt
def process_attendance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get address from coordinates
        geolocator = Nominatim(user_agent="attendance_app")
        location = geolocator.reverse(f"{data['latitude']}, {data['longitude']}")
        address = location.address if location else "Unknown"

        is_check_in = True  # Implement your logic here

        message = f"{'Check-in' if is_check_in else 'Check-out'} recorded:\n" \
                  f"Name: {data['user_name']}\n" \
                  f"Employee ID: {data['employee_id']}\n" \
                  f"Time: {data['scan_time']}\n" \
                  f"Address: {address}\n" \
                  f"GPS: {data['latitude']}, {data['longitude']}"

        # Send to Telegram group
        send_to_telegram_group(message)

        return JsonResponse({'status': 'success', 'message': 'Attendance recorded successfully'})
    return JsonResponse({'status': 'error'}, status=400)
