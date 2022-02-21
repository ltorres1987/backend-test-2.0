import pytest

from datetime import datetime
from unittest.mock import Mock

from src.user.entities.user import User
from src.user.usecases.manage_user_usecase import ManageUserUsecase

# Pruebas para el caso de uso del el manejo de user, usando un Mock
# para simular el repositorio de Firestore, es decir, en este caso no se utiliza el emulador.


@pytest.fixture
def repository_mock():
    return Mock()


@pytest.fixture
def manage_user_usecase(repository_mock):
    return ManageUserUsecase(repository_mock)


class TestManageUserUsecase:

    def test_get_user(self, manage_user_usecase):

        # Definir que el mock del repositorio retorne tres user.

        mock_users = [
            User(1, "sport line", "venta de ropa deportiva", "latc", "ec"),
            User(2, "troncalnet", "venta de ropa deportiva", "latc", "ec"),
            User(3, "sport line", "venta de ropa deportiva", "latc", "ec"),
        ]

        manage_user_usecase.user_repository.get_users.return_value = mock_users

        # Obtener los user desde el caso de uso, y afirmar que se haya
        # retornado la cantidad correcta de user.

        users = manage_user_usecase.get_users()
        
        assert len(users) == len(mock_users)

    def test_create_user(self, manage_user_usecase):

        # Definir que el mock del repositorio retorne un user.

        mock_id = 25

        data = {
            "name": "test",
            "email": "test",
            "city": "test",
            "address": "test",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        
        mock_user = User.from_dict(data)
        mock_user.id = mock_id
        
        manage_user_usecase.user_repository.create_user.return_value = mock_user

        # Crear un user con el caso de uso.
        
        user = manage_user_usecase.create_user(data)

        # Afirmar que el user retornado tenga los mismos datos definidos.
        
        assert user.id == mock_id
        assert user.name == data["name"]
        assert user.email == data["email"]
        assert user.city == data["city"]
        assert user.address == data["address"]
