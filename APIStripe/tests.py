import json
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from APIStripe.models import Item
from APIStripe.views import CreateCheckoutSessionView

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

        self.data_nokia_3310 = {"name": "Nokia 3310", "descr": "device 4", "cost": "150", "currently": "usd"}
        self.nokia_3600_slider = {"name": "Nokia 3600 slider", "descr": "device 5", "cost": "250", "currently": "usd"}
        self.nokia_6300 = {"name": "Nokia 6300", "descr": "device 6", "cost": "200", "currently": "usd"}

        self.data_nokia_3310["id"] = str(self.__add_poroduct(self.data_nokia_3310))
        self.nokia_3600_slider["id"] = str(self.__add_poroduct(self.nokia_3600_slider))
        self.nokia_6300["id"] = str(self.__add_poroduct(self.nokia_6300))

    
    def test_create_checkout_session_view(self):

        product = self.data_nokia_3310

        factory = RequestFactory()
        
        request = factory.get('', {
            'currently': product['currently']
        })

        request.META['HTTP_REFERER'] = 'http://localhost:8000/'
        request.META['HTTP_USER_AGENT'] = 'testing_agent'

        request.user = self.user
        response = CreateCheckoutSessionView.as_view()(request, id=product['id'])

        data = json.loads(response.content)
        result_test = 'id' in data

        if result_test:
            self.color_print("id: " + data["id"])
      

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result_test, True)