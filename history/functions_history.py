import json

from history.models import HistoryItem

HISTORY_STATUS_SUCCESS = "success"
HISTORY_STATUS_FAILED = "failed"
HISTORY_STATUS_CANCEL = "cancel"
HISTORY_STATUS_EXPECTATION = "expectation"

def prepare_data(name, cost, count):
    return json.dumps(
        {
            "total_cost": str(cost),
            "products": [{
                "name": name,
                "cost": str(cost),
                "count": str(count)
            }]
        }
    )

def prepare_array(data):

    result = []
    total_cost = 0

    for item in data:
        price_data = item["price_data"]
        price = int(price_data["unit_amount"]) / 100.0
        total_cost += float(price * int(item["quantity"]))

        result.append({
            "name": price_data["product_data"]["name"],
            "cost": price,
            "count": item["quantity"]
        })

    return json.dumps({
            "total_cost": str(total_cost),
            "products": result
        })



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
