
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

