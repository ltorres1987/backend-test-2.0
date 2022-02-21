from datetime import datetime

from src.product.entities.product import Product


class TestProduct:

    def test_to_dict(self):

        # Crear instancia del product.

        id = "1"
        name = "test"
        short_description = "test"
        quantity = 12
        seller_id = 13

        product = Product(id, name, short_description, quantity, seller_id)

        # Obtener diccionario y afirmar que sean iguales los datos.

        dict = product.to_dict()

        assert dict["id"] == id
        assert dict["name"] == name
        assert dict["short_description"] == short_description
        assert dict["quantity"] == quantity
        assert dict["seller_id"] == seller_id

    def test_serialize(self):

        # Crear instancia del product con fechas.

        id = "1"
        name = "test"
        short_description = "test"
        quantity = 12
        seller_id = 13
        created_at = datetime(year=2022, month=2, day=25, hour=10, minute=24, second=13, microsecond=321654)
        updated_at = datetime(year=2022, month=2, day=25, hour=10, minute=24, second=14, microsecond=321654)
        deleted_at = datetime(year=2022, month=2, day=25, hour=10, minute=24, second=15, microsecond=321654)

        product = Product(id, name, short_description, quantity, seller_id, created_at, updated_at, deleted_at)

        # Obtener diccionario serializable y afirmar que sean iguales los datos,
        # que las fechas vengan formateadas y que no venga con fecha de borrado.

        data = product.serialize()

        assert data["id"] == id
        assert data["name"] == name
        assert data["short_description"] == short_description
        assert data["quantity"] == quantity
        assert data["seller_id"] == seller_id
        assert data["created_at"] == "2022-02-25 10:24:13"
        assert data["updated_at"] == "2022-02-25 10:24:14"
        assert "deleted_at" not in data

    def test_from_dict(self):

        # Crear diccionario de datos.

        dict = {
            "id": "2",
            "name": "test",
            "short_description": "test",
            "quantity": 12,
            "seller_id": 13,
        }

        # Obtener instancia desde diccionario y afirmar que sean iguales los datos.

        product = Product.from_dict(dict)

        assert product.id == dict["id"]
        assert product.name == dict["name"]
        assert product.short_description == dict["short_description"]
        assert product.quantity == dict["quantity"]
        assert product.seller_id == dict["seller_id"]
