import base64

from django.test import TestCase
from rest_framework.test import APIClient

from orders_app.enums import OrderStatus
from orders_app.models import Product, Order, Bill


class CashierTest(TestCase):
    fixtures = ['cashier_user_fixture.json', 'order_after_execution_fixture.json']

    def setUp(self):
        self.client = APIClient()
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Basic {base64.b64encode(b"cashier:123").decode("ascii")}'

    def test_create_product(self):
        product_data = {
            "name": "Product",
            "price": 123.12
        }
        response = self.client.post('/product/', product_data)
        self.assertEqual(response.status_code, 201)
        return Product.objects.get(pk=response.json().get('id'))

    def test_create_order(self):
        product = self.test_create_product()
        response = self.client.post('/order/', {'product': product.id})
        self.assertEqual(response.status_code, 201)
        return Order.objects.get(pk=response.json().get('id'))

    def test_create_bill(self):
        executed_order = Order.objects.get(status=OrderStatus.EXECUTED.value)
        response = self.client.post('/bill/', {'order': executed_order.id})
        self.assertEqual(response.status_code, 201)
        return Bill.objects.get(order_id=executed_order.id)

    def test_view_bill(self):
        bill = self.test_create_bill()
        response = self.client.get(f'/bill/{bill.id}/')
        self.assertEqual(response.status_code, 200)

    def test_bill_order(self):
        order = Order.objects.get(status=OrderStatus.EXECUTED.value)
        self.assertEqual(order.status, OrderStatus.EXECUTED.value)
        response = self.client.patch(f'/order/{order.id}/', {'status': OrderStatus.BILLED.value})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), OrderStatus.BILLED.value)


class SalesConsultantTest(TestCase):
    fixtures = ['sales_consultant_user_fixture.json', 'order_after_creation_fixture.json']

    def setUp(self):
        self.client = APIClient()
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Basic {base64.b64encode(b"sales_consultant:123").decode("ascii")}'

    def test_view_order(self):
        order = Order.objects.get(status=OrderStatus.OPENED.value)
        response = self.client.get(f'/order/{order.id}/')
        self.assertEqual(response.status_code, 200)

    def test_execute_order(self):
        order = Order.objects.get(status=OrderStatus.OPENED.value)
        self.assertEqual(order.status, OrderStatus.OPENED.value)
        response = self.client.patch(f'/order/{order.id}/', {'status': OrderStatus.EXECUTED.value})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), OrderStatus.EXECUTED.value)


class AccountantTest(TestCase):
    fixtures = ['accountant_user_fixture.json', 'orders_fixture.json']

    def setUp(self):
        self.client = APIClient()
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Basic {base64.b64encode(b"accountant:123").decode("ascii")}'

    def test_view_orders(self):
        response = self.client.get(f'/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('results')), 3)
        # from 2021-08-28
        response = self.client.get(f'/orders/?start_date=2021-08-28')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('results')), 2)
        # to 2021-08-28
        response = self.client.get(f'/orders/?end_date=2021-08-28')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('results')), 1)
        # from 2020-08-28 to 2021-08-28
        response = self.client.get(f'/orders/?start_date=2020-08-28&end_date=2021-08-28')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('results')), 1)
