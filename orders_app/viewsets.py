from datetime import datetime, date

from rest_framework import viewsets, mixins
from django.db.models import Q

from order_management_project.generic import method_permission_classes
from orders_app.models import Product, Order, Bill
from orders_app.permissions import OrderCreate, OrderView, OrderStatusChange, GenerateBill
from orders_app.serializers import ProductSerializer, OrderSerializer, OrderStatusWriteSerializer, \
    OrderRetrieveSerializer, BillCreateSerializer, BillRetrieveSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Viewset for Product model.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_permission_classes((OrderCreate,))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Viewset for Order model.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        serializers = {
            'partial_update': OrderStatusWriteSerializer,
            'list': OrderRetrieveSerializer,
        }
        return serializers.get(self.action, self.serializer_class)

    def get_queryset(self):
        if self.action == 'list':
            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            return self._query_by_date(start_date, end_date)
        return super().get_queryset()

    @staticmethod
    def _convert_to_date(datetime_str: str) -> date:
        """
        Method to convert string into date object
        """

        return datetime.strptime(datetime_str, '%Y-%m-%d').date()

    def _query_by_date(self, start_date: str = None, end_date: str = None):
        """
        Method to filter queryset by date
        """

        _filters = Q()
        if start_date:
            start_date = self._convert_to_date(start_date)
            _filters &= Q(created_at__gte=start_date)

        if end_date:
            end_date = self._convert_to_date(end_date)
            _filters &= Q(created_at__lte=end_date)

        return self.queryset.filter(_filters)

    @method_permission_classes((OrderCreate,))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_permission_classes((OrderView,))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_permission_classes((OrderView,))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_permission_classes((OrderStatusChange,))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class BillViewSet(viewsets.ModelViewSet):
    """
    Viewset for Bill model.
    """

    queryset = Bill.objects.all()
    serializer_class = BillRetrieveSerializer

    def get_serializer_class(self):
        serializers = {
            'create': BillCreateSerializer,
            'retrieve': BillRetrieveSerializer,
        }
        return serializers.get(self.action)

    @method_permission_classes((GenerateBill,))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_permission_classes((GenerateBill,))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
