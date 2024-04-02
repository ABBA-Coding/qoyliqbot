# store/views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from .models import Category, Product, Order
from django.utils.translation import activate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer

from ..address.models import Address
from ..users.models import TelegramUser


def category_list(request):
    categories = Category.objects.filter(is_active=True)
    language = request.GET.get('lang', 'uz')
    activate(language)
    return render(request, 'products/category_list.html', {'categories': categories})


def product_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category, is_active=True)
    language = request.GET.get('lang', 'uz')
    activate(language)
    return render(request, 'products/product_list.html', {'category': category, 'products': products})


def get_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    language = request.GET.get('lang', 'uz')
    activate(language)
    data = {
        'id': product.pk,
        'price': product.price,
        'name': product.name,
        'image': product.image.url if product.image else '/static/images/not_found.jpeg',
        'count': 1
    }
    return JsonResponse(data)


def get_user(request, user_id):
    user = get_object_or_404(TelegramUser, pk=user_id)
    language = request.GET.get('lang', 'uz')
    activate(language)

    # Fetching the user's addresses
    addresses = Address.objects.filter(user=user)

    # Creating a list of address data
    address_list = []
    for address in addresses:
        address_data = {
            'id': address.pk,
            'name': address.name,
            'longitude': address.longitude,
            'latitude': address.latitude,
        }
        address_list.append(address_data)

    data = {
        'id': user.pk,
        'fullname': user.fullname,
        'addresses': address_list,  # Adding addresses to the response
    }
    return JsonResponse(data)


def cart(request):
    # Retrieve cart data from session storage
    language = request.GET.get('lang', 'uz')
    activate(language)

    # Pass cart data to the template
    return render(request, 'products/cart.html')


def order(request):
    # Retrieve cart data from session storage
    language = request.GET.get('lang', 'uz')
    activate(language)

    # Pass cart data to the template
    return render(request, 'products/order.html')


@api_view(['POST'])
def create_order(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOrderAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
