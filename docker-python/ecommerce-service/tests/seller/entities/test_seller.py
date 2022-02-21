from datetime import datetime

from src.seller.entities.seller import Seller


class TestSeller:

    def test_to_dict(self):

        # Crear instancia del seller.

        id = "1"
        name = "test"
        short_description = "test"
        seller_user = "test"
        address = "test"

        seller = Seller(id, name, short_description, seller_user, address)

        # Obtener diccionario y afirmar que sean iguales los datos.

        dict = seller.to_dict()

        assert dict["id"] == id
        assert dict["name"] == name
        assert dict["short_description"] == short_description
        assert dict["seller_user"] == seller_user
        assert dict["address"] == address

    def test_serialize(self):

        # Crear instancia del seller con fechas.

        id = "1"
        name = "test"
        short_description = "test"
        seller_user = "test"
        address = "test"
        created_at = datetime(year=2022, month=2, day=25, hour=10, minute=24, second=13, microsecond=321654)
        updated_at = datetime(year=2022, month=2, day=25, hour=10, minute=24, second=14, microsecond=321654)
        deleted_at = datetime(year=2022, month=2, day=25, hour=10, minute=24, second=15, microsecond=321654)

        seller = Seller(id, name, short_description, seller_user, address, created_at, updated_at, deleted_at)

        # Obtener diccionario serializable y afirmar que sean iguales los datos,
        # que las fechas vengan formateadas y que no venga con fecha de borrado.

        data = seller.serialize()

        assert data["id"] == id
        assert data["name"] == name
        assert data["short_description"] == short_description
        assert data["seller_user"] == seller_user
        assert data["address"] == address
        assert data["created_at"] == "2022-02-25 10:24:13"
        assert data["updated_at"] == "2022-02-25 10:24:14"
        assert "deleted_at" not in data

    def test_from_dict(self):

        # Crear diccionario de datos.

        dict = {
            "id": "2",
            "name": "test",
            "short_description": "test",
            "seller_user": "test",
            "address": "test",
        }

        # Obtener instancia desde diccionario y afirmar que sean iguales los datos.

        seller = Seller.from_dict(dict)

        assert seller.id == dict["id"]
        assert seller.name == dict["name"]
        assert seller.short_description == dict["short_description"]
        assert seller.seller_user == dict["seller_user"]
        assert seller.address == dict["address"]
