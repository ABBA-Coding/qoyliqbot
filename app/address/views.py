import json

from django.http import JsonResponse
from django.utils.translation import activate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.address.serializers import AddressSerializer
from bot.functions import get_location_name

from app.address.models import Branch, Address


def get_branches(request):
    branches = Branch.objects.filter(is_active=True)
    language = request.GET.get('lang', 'uz')
    activate(language)
    data = [{'id': a.pk, 'name': a.name, 'longitude': a.longitude, 'latitude': a.latitude} for a in branches]
    return JsonResponse({"data": data})


@csrf_exempt
def get_address(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from request body
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        try:
            address_name = get_location_name(latitude, longitude)
            address, _created = Address.objects.get_or_create(user_id=user_id,
                                                              name=address_name,
                                                              defaults={"latitude": latitude,
                                                                        "longitude": longitude})

            address_data = {
                'id': address.pk,
                'name': address.name,
                'longitude': address.longitude,
                'latitude': address.latitude,
            }
            print(address)
            return JsonResponse(address_data)
        except Address.DoesNotExist:
            return JsonResponse({'error': 'Address not found'}, status=404)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
