import json
import sys
from django.urls import resolve

def getCurrentHost(request):
    return request.META['HTTP_REFERER']

def get_app_name(request):
    return sys.modules[resolve(request.path_info).func.__module__].__package__

class ModelJsonData:

    def get_data(self, model, user_id, from_field):
        data = model.objects.filter(user_id=user_id).values(from_field).first()

        if data:
            data = data.get(from_field)
            return json.loads(data)

        return []

    def set_data(self, model, user_id, to_field, array):
        
        updated_values = {
            to_field : json.dumps(list(dict.fromkeys(array)))
            }

        result = model.objects.update_or_create(
            user_id = user_id,
            defaults = updated_values
        )

        return result[0].pk