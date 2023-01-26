import pytest

def test_create_order_service(client, order_uri, order):
    response = client.post(order_uri, json=order)
    pytest.assume(response.status.startswith('200'))
    returned_order = response.json
    for param, value in order.items():
        pytest.assume(returned_order[param] == value)