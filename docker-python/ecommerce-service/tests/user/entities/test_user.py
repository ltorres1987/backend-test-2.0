from datetime import datetime

from src.user.entities.user import User


class TestUser:

    def test_to_dict(self):

        # Crear instancia del user.

        id = "1"
        name = "test"
        email = "test"
        city = "test"
        address = "test"

        user = User(id, name, email, city, address)

        # Obtener diccionario y afirmar que sean iguales los datos.

        dict = user.to_dict()

        assert dict["id"] == id
        assert dict["name"] == name
        assert dict["email"] == email
        assert dict["city"] == city
        assert dict["address"] == address

    def test_serialize(self):

        # Crear instancia del user con fechas.

        id = "1"
        name = "test"
        email = "test"
        city = "test"
        address = "test"
        created_at = datetime(year=2022, month=2, day=25, hour=10, minute=24, second=13, microsecond=321654)
        updated_at = datetime(year=2022, month=2, day=25, hour=10, minute=24, second=14, microsecond=321654)
        deleted_at = datetime(year=2022, month=2, day=25, hour=10, minute=24, second=15, microsecond=321654)

        user = User(id, name, email, city, address, created_at, updated_at, deleted_at)

        # Obtener diccionario serializable y afirmar que sean iguales los datos,
        # que las fechas vengan formateadas y que no venga con fecha de borrado.

        data = user.serialize()

        assert data["id"] == id
        assert data["name"] == name
        assert data["email"] == email
        assert data["city"] == city
        assert data["address"] == address
        assert data["created_at"] == "2022-02-25 10:24:13"
        assert data["updated_at"] == "2022-02-25 10:24:14"
        assert "deleted_at" not in data

    def test_from_dict(self):

        # Crear diccionario de datos.

        dict = {
            "id": "2",
            "name": "test",
            "email": "test",
            "city": "test",
            "address": "test",
        }

        # Obtener instancia desde diccionario y afirmar que sean iguales los datos.

        user = User.from_dict(dict)

        assert user.id == dict["id"]
        assert user.name == dict["name"]
        assert user.email == dict["email"]
        assert user.city == dict["city"]
        assert user.address == dict["address"]
