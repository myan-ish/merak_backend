from decimal import Decimal
import pytest
from audit.models import EntryItem, Ledger
from inventory.models import Product
from user.models import Customer, User
from django.test.client import Client
from rest_framework.test import APIClient

client = Client()


@pytest.fixture
def admin(db):
    return User.objects.create_user(
        email="admin@test.com", password="test", status="Active"
    )


@pytest.fixture
def ledger():
    return Ledger.objects.create(
        name="Test Ledger", customer=Customer.objects.create(name="Test Customer")
    )


@pytest.fixture
def product():
    return Product.objects.create(name="Test Product", price=100, quantity=100)


@pytest.fixture
def entry_item(product):
    return EntryItem.objects.create(product=product, quantity=10, price=100)


@pytest.fixture
def admin_token(admin):
    response = client.post(
        "/api/user/auth/login/", {"email": "admin@test.com", "password": "test"}
    )
    print(response)
    return response.data.get("access")


@pytest.fixture
def regular_client(admin_token):
    c = APIClient()
    c.credentials(HTTP_AUTHORIZATION="Bearer " + str(admin_token))
    return c


@pytest.mark.django_db
def test_ledger_make_empty_transaction(ledger):
    ledger.make_transaction([], "SI", 0, 0)
    assert ledger.closing_balance == 0


@pytest.mark.django_db
def test_ledger_make_debit_transaction(ledger, entry_item):
    ledger.make_transaction(
        [
            entry_item.id,
        ],
        "SI",
        0,
        0,
    )
    assert ledger.closing_balance == 1130


@pytest.mark.django_db
def test_ledger_make_credit_transaction(ledger, entry_item):
    ledger.make_transaction(
        [
            entry_item.id,
        ],
        "SR",
        0,
        0,
    )
    assert ledger.closing_balance == -1130


@pytest.mark.django_db
def test_ledger_make_credit_transaction_with_discount(ledger, entry_item):
    ledger.make_transaction(
        [
            entry_item.id,
        ],
        "SR",
        0,
        100,
    )
    assert ledger.closing_balance == -1130


@pytest.mark.django_db
def test_ledger_make_credit_transaction_with_vatable_discount(ledger, entry_item):
    ledger.make_transaction(
        [
            entry_item.id,
        ],
        "SR",
        100,
        0,
    )
    assert ledger.closing_balance == -1030


@pytest.mark.django_db
def test_ledger_make_credit_transaction_with_vatable_and_non_vatable_discount(
    ledger, entry_item
):
    ledger.make_transaction(
        [
            entry_item.id,
        ],
        "SR",
        100,
        100,
    )
    assert ledger.closing_balance == -1030


@pytest.mark.django_db
def test_transaction_api(regular_client, ledger, product):

    data = {
        "customer": ledger.customer.id,
        "type": "SI",
        "items": [
            {"product": product.id, "quantity": 100, "price": 10},
        ],
        "vatable_discount": 100,
        "non_vatable_discount": 100,
    }

    response = regular_client.post("/api/audit/transaction/", data=data, format="json")
    assert response.data.get("closing_balance") == 1030


# from audit.models import Ledger, Entry
# from user.models import Customer, Organization, User
# # @pytest.fixture
# # def entry(db):
# #     return Entry.objects.create(
# #         ledger = Ledger.objects.create(name = "test"),
# #         amount = 100,
# #         description = "test",
# #         type = "Credit",
# #         date = "2020-01-01"
# #     )

# @pytest.fixture
# def organization(db):
#     return Organization.objects.create(name = "test", owner=User.objects.create_user(email="test@test.com", password="test12345"))

# @pytest.fixture
# def customer(db, organization):
#     return Customer.objects.create(
#         name = "test",organization=organization)

# @pytest.fixture
# def ledger(db, customer):
#     return  Ledger.objects.create(name = "test", type="CAPITAL", opening_balance=100, closing_balance=100, related_user=customer)

# @pytest.mark.django_db
# def test_ledger_transaction_credit(ledger):
#     ledger.make_transaction(100, True, "Credit")
#     assert ledger.closing_balance == 200

# @pytest.mark.django_db
# def test_ledger_transaction_debit(ledger):
#     ledger.make_transaction(100, False, "Debit")
#     assert ledger.closing_balance == 0
