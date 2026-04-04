def create_customer(connection, customer_data: dict) -> int:
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO oc_customer (
            customer_group_id,
            store_id,
            language_id,
            firstname,
            lastname,
            email,
            telephone,
            password,
            custom_field,
            ip,
            token,
            code,
            status,
            safe,
            newsletter,
            date_added
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """

        cursor.execute(sql, (
            1,
            0,
            1,
            customer_data["firstname"],
            customer_data["lastname"],
            customer_data["email"],
            customer_data["telephone"],
            "test123",
            "{}",
            "127.0.0.1",
            "",
            "",
            1,
            0,
            0
        ))

        return cursor.lastrowid


def get_customer_by_id(connection, customer_id: int):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM oc_customer WHERE customer_id = %s"
        cursor.execute(sql, (customer_id,))
        return cursor.fetchone()


def update_customer_by_id(connection, customer_id: int, data: dict) -> int:
    with connection.cursor() as cursor:
        sql = """
        UPDATE oc_customer
        SET firstname=%s, lastname=%s, email=%s, telephone=%s
        WHERE customer_id=%s
        """
        result = cursor.execute(sql, (
            data["firstname"],
            data["lastname"],
            data["email"],
            data["telephone"],
            customer_id
        ))
        return result


def delete_customer_by_id(connection, customer_id: int) -> int:
    with connection.cursor() as cursor:
        sql = "DELETE FROM oc_customer WHERE customer_id = %s"
        result = cursor.execute(sql, (customer_id,))
        return result