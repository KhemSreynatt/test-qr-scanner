
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def qr_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = data.get('result')
        # Process the result as needed
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)