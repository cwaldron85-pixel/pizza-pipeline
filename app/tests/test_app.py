import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app, GarlicBread, TOPPINGS

def test_app_exists():
    assert app is not None

def test_app_has_a_name():
    assert app.name == "app"

def test_garlic_bread_price():
    gb = GarlicBread()
    assert gb.price == 4.99

def test_toppings_dict_not_empty():
    assert len(TOPPINGS) > 0

def test_homepage_status_code():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
