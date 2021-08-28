from rest_framework import serializers

from orders_app.models import Product, Order, Bill
from orders_app.validators import is_order_executed


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class for Product model.
    """

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('discount',)


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer class for Order model.
    """

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status',)


class OrderStatusWriteSerializer(serializers.ModelSerializer):
    """
    Serializer class for changing status of Order model instance.
    """

    class Meta:
        model = Order
        fields = ('status',)


class OrderRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer class to retrieve Order model instance.
    """

    product = ProductSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'discount', 'product')


class OrderForBillSerializer(serializers.ModelSerializer):
    """
    Serializer class to retrieve Product model instance with fields special for bill
    """

    class Meta:
        model = Order
        fields = ('created_at',)


class ProductForBillSerializer(serializers.ModelSerializer):
    """
    Serializer class to retrieve Product model instance with fields special for bill
    """
    price_with_discount = serializers.SerializerMethodField()

    @staticmethod
    def get_price_with_discount(obj):
        if obj.discount != 0:
            return obj.price * obj.discount / 100.0
        return obj.price

    class Meta:
        model = Product
        fields = ('name', 'price', 'price_with_discount')
        read_only_fields = ('name', 'price', 'price_with_discount')


class BillCreateSerializer(serializers.ModelSerializer):
    """
    Serializer class to create Bill model instance.
    """

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if not is_order_executed(data.get('order')):
            raise serializers.ValidationError("Order in not executed")
        return data

    class Meta:
        model = Bill
        fields = ('order',)


class BillRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer class to retrieve Bill model instance.
    """

    product = serializers.SerializerMethodField()
    order = OrderForBillSerializer()

    @staticmethod
    def get_product(obj):
        return ProductForBillSerializer(obj.order.product).data

    class Meta:
        model = Bill
        fields = ('created_at', 'order', 'product')
        read_only_fields = ('product', 'order')
