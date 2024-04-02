from rest_framework import serializers
from .models import Order, SelectedProduct


class OrderSerializer(serializers.ModelSerializer):
    selected_products = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        selected_products_data = validated_data.pop('selected_products', None)
        order = super().create(validated_data)
        if selected_products_data:
            for product_data in selected_products_data:
                SelectedProduct.objects.create(order=order, **product_data)
        return order
