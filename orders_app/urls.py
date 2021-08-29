from django.urls import path

from orders_app.viewsets import OrderViewSet, ProductViewSet, BillViewSet

urlpatterns = [
    path('order/', OrderViewSet.as_view({'post': 'create'})),
    path('order/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
    path('orders/', OrderViewSet.as_view({'get': 'list'})),

    path('product/', ProductViewSet.as_view({'post': 'create'})),

    path('bill/', BillViewSet.as_view({'post': 'create'})),
    path('bill/<int:pk>/', BillViewSet.as_view({'get': 'retrieve'})),
]
