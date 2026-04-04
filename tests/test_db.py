from faker import Faker

from scr.utils import create_customer, delete_customer_by_id, get_customer_by_id, update_customer_by_id
import faker

def test_create_customer(connection):
    data = {
        "firstname": Faker().first_name(),
        "lastname": Faker().last_name(),
        "email": Faker().email(),
        "telephone": Faker().phone_number()
    }

    customer_id = create_customer(connection, data)
    customer = get_customer_by_id(connection, customer_id)

    assert customer is not None
    assert customer["firstname"] == data["firstname"]


def test_update_customer(connection):
    data = {
        "firstname": Faker().first_name(),
        "lastname": Faker().last_name(),
        "email": Faker().email(),
        "telephone": Faker().phone_number()
    }

    customer_id = create_customer(connection, data)

    updated_data = {
        "firstname": Faker().first_name(),
        "lastname": Faker().last_name(),
        "email": Faker().email(),
        "telephone": Faker().phone_number()
    }

    result = update_customer_by_id(connection, customer_id, updated_data)
    customer = get_customer_by_id(connection, customer_id)

    assert result == 1
    assert customer["firstname"] == updated_data.get("firstname")


def test_update_nonexistent_customer(connection):
    result = update_customer_by_id(connection, Faker().random_int(), {
        "firstname": Faker().first_name(),
        "lastname": Faker().last_name(),
        "email": Faker().email(),
        "telephone": Faker().phone_number()
    })

    assert result == 0


def test_delete_customer(connection):
    data = {
        "firstname": Faker().first_name(),
        "lastname": Faker().last_name(),
        "email": Faker().email(),
        "telephone": Faker().phone_number()
    }

    customer_id = create_customer(connection, data)
    result = delete_customer_by_id(connection, customer_id)
    customer = get_customer_by_id(connection, customer_id)

    assert result == 1
    assert customer is None


def test_delete_nonexistent_customer(connection):
    result = delete_customer_by_id(connection, Faker().random_int())
    assert result == 0