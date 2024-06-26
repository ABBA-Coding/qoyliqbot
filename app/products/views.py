from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from .models import Category, Product, Order
from django.utils.translation import activate
from rest_framework.decorators import api_view
from .serializers import OrderSerializer

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from asgiref.sync import async_to_sync

from app.products.models import SelectedProduct
from bot.misc import bot
from bot.utils.kbs import approve
from rest_framework import status
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Call send_new_user_notification function after order creation
        instance = serializer.instance
        send_new_user_notification(instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def send_new_user_notification(instance):
    sync_send_message = async_to_sync(bot.send_message)
    # Prepare message data
    selected_products = SelectedProduct.objects.filter(order=instance)
    products_text = "\n".join([f"{product.name}: {product.count}" for product in selected_products])

    success_text = str(_("<b>Yangi buyurtma</b>\n"
                         "Jami: {all_cost}\n"
                         "Foydalanuvchi: {user}\n"
                         "Mahsulotlar:\n{products}\n"
                         )).format(
        all_cost=instance.all_cost,
        user=instance.user.phone if instance.user else None,
        products=products_text,
    )
    sync_send_message(instance.user_id, success_text)
    sync_send_message(settings.TELEGRAM_GROUP_ID, success_text, reply_markup=approve(instance.pk))
