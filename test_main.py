from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_items_crud():
    # Create item
    response = client.post("/items/", json={"name": "RouterItem", "price": 1.23, "is_offer": False})
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "RouterItem"
    item_id = item["id"]

    # Get item
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "RouterItem"

    # List items
    response = client.get("/items/")
    assert response.status_code == 200
    assert any(i["id"] == item_id for i in response.json())

def test_orders_crud():
    # Create item for order
    response = client.post("/items/", json={"name": "OrderRouterItem", "price": 9.99, "is_offer": False})
    item_id = response.json()["id"]

    # Create order
    response = client.post("/orders/", json={"items": [{"item_id": item_id, "quantity": 3}]})
    assert response.status_code == 200
    order = response.json()
    order_id = order["id"]

    # Get order
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    order_data = response.json()
    assert order_data["id"] == order_id
    assert order_data["items"][0]["item_id"] == item_id
    assert order_data["items"][0]["quantity"] == 3

    # List orders
    response = client.get("/orders/")
    assert response.status_code == 200
    assert any(o["id"] == order_id for o in response.json())

    # Delete order
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 204

    # Confirm deletion
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 404