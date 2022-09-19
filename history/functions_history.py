import json

from history.models import HistoryItem

HISTORY_STATUS_SUCCESS = "success"
HISTORY_STATUS_FAILED = "failed"
HISTORY_STATUS_CANCEL = "cancel"
HISTORY_STATUS_EXPECTATION = "expectation"

def prepare_data(name, cost, count):
    return json.dumps([{
        "name": name,
        "cost": str(cost),
        "count": str(count)
    }])

def prepare_array(data):

    result = []

    for item in data:

        result.append({
            "name": item["price_data"]["product_data"]["name"],
            "cost": item["price_data"]["unit_amount"],
            "count": item["quantity"]
        })

    return json.dumps(result)



def set_history(user_id, data, currently):

    history = HistoryItem(
        user_id=user_id, 
        data=data, 
        currency=currently
    )

    history.save()
    return history.id


def update_status(id, status):

    if not id:
        return False

    return HistoryItem.objects.filter(id=id).update(status=status)
