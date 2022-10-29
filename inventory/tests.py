import pytest

from inventory.models import Product

@pytest.fixture
def test_proudct():
    return Product.objects.create(name="test", price=10, quantity=10)

@pytest.mark.django_db
def test_add_stock(test_proudct):
    test_proudct.add_stock(10, 10)
    assert test_proudct.quantity == 20
    assert test_proudct.price == 10

    test_proudct.add_stock(10, 20)
    assert test_proudct.quantity == 40
    assert test_proudct.price == 10