import pytest
from faker import Faker

from scr.utils import create_customer, delete_customer_by_id, get_customer_by_id, update_customer_by_id


def make_customer_data() -> dict:
    return {
        "firstname": Faker().first_name(),
        "lastname": Faker().last_name(),
        "email": Faker().email(),
        "telephone": Faker().phone_number(),
    }


@pytest.fixture()
def customer_data() -> dict:
    return make_customer_data()


@pytest.fixture()
def created_customer(connection, customer_data) -> int:
    customer_id = create_customer(connection, customer_data)
    yield customer_id
    delete_customer_by_id(connection, customer_id)


def test_create_customer(connection):
    data = make_customer_data()
    customer_id = create_customer(connection, data)
    customer = get_customer_by_id(connection, customer_id)
    assert customer is not None
    assert customer["firstname"] == data["firstname"]


def test_update_customer(connection, created_customer):
    updated_customer_data = make_customer_data()
    result = update_customer_by_id(connection, created_customer, updated_customer_data)
    customer = get_customer_by_id(connection, created_customer)

    assert result == 1
    assert customer["firstname"] == updated_customer_data.get("firstname")


def test_update_nonexistent_customer(connection):
    result = update_customer_by_id(connection, Faker().random_int(1000,9999,1), make_customer_data())

    assert result == 0


def test_delete_customer(connection, created_customer):
    result = delete_customer_by_id(connection, created_customer)
    customer = get_customer_by_id(connection, created_customer)

    assert result == 1
    assert customer is None


def test_delete_nonexistent_customer(connection):
    c_id = Faker().random_int()
    result = delete_customer_by_id(connection, c_id)
    assert result == 0
