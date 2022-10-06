import json
import time
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from APIStripe.models import Item
from APIStripe.views import (
    BasketCreateCheckoutSessionView, 
    CreateCheckoutSessionView
)

COLOR_GREEN  = '\33[32m'
COLOR_END = '\033[0m'

User = get_user_model()

class APIStripeTestcases(TestCase):

    def color_print(self, text, color=COLOR_GREEN):
        print(color + str(text) + COLOR_END)

    def __add_poroduct(self, product: set):

        data = Item.objects.filter(name=product["name"])

        if not data.exists():
            result = Item.objects.create(name=product["name"], description=product["descr"], price=int(product["cost"]))
            result.save()
            return result.id

        return data[0].id

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')

        self.data_nokia_3310 = {"name": "Nokia 3310", "descr": "device 4", "cost": "150", "currency": "usd"}
        self.nokia_3600_slider = {"name": "Nokia 3600 slider", "descr": "device 5", "cost": "250", "currency": "usd"}
        self.nokia_6300 = {"name": "Nokia 6300", "descr": "device 6", "cost": "200", "currency": "usd"}

        self.data_nokia_3310["id"] = str(self.__add_poroduct(self.data_nokia_3310))
        self.nokia_3600_slider["id"] = str(self.__add_poroduct(self.nokia_3600_slider))
        self.nokia_6300["id"] = str(self.__add_poroduct(self.nokia_6300))


    def __get_data_to_basket(self, product: set, count: int) -> set:
        return {
            'price_data': {
                'currency': product['currency'],
                'product_data': {
                    'name': product['name'],
                },
                'unit_amount': product['cost'],
            },
            'quantity': str(count),
        }


    def get_result_stripe_api(self, response_content):
        
        data = json.loads(response_content)
        result_test = 'id' in data

        if result_test:
            self.color_print("\nid: " + data["id"])

        return result_test

    
    def test_create_checkout_session_view(self):

        product = self.data_nokia_3310

        factory = RequestFactory()
        
        request = factory.get('', {
            'currently': product['currency']
        })

        request.META['HTTP_REFERER'] = 'http://localhost:8000/'
        request.META['HTTP_USER_AGENT'] = 'testing_agent'

        request.user = self.user

        start = time.perf_counter()
        response = CreateCheckoutSessionView.as_view()(request, id=product['id'])
        result_time = time.perf_counter() - start

        result_test = self.get_result_stripe_api(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result_test, True)

        self.color_print("\nCreateCheckoutSessionView execution time: " + str(result_time))

    def test_basket_create_checkout_session_view(self):

        array_data = []
        array_data.append(self.__get_data_to_basket(self.data_nokia_3310, 2))
        array_data.append(self.__get_data_to_basket(self.nokia_3600_slider, 1))
        array_data.append(self.__get_data_to_basket(self.nokia_6300, 3))

        array_ids = []
        array_ids.append(self.data_nokia_3310["id"])
        array_ids.append(self.nokia_3600_slider["id"])
        array_ids.append(self.nokia_6300["id"])

        factory = RequestFactory()
        
        request = factory.post('', {
                'data': array_data,
                'ids': array_ids
            },
            'application/json'
        )

        request.META['HTTP_ORIGIN'] = 'http://localhost:8000/'
        request.META['HTTP_USER_AGENT'] = 'testing_agent'

        request.user = self.user

        start = time.perf_counter()
        response = BasketCreateCheckoutSessionView.as_view()(request)
        result_time = time.perf_counter() - start

        result_test = self.get_result_stripe_api(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result_test, True)

        self.color_print("\nBasketCreateCheckoutSessionView execution time: " + str(result_time))