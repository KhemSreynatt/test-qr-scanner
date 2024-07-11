
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

