import pytest

from datetime import datetime
from unittest.mock import Mock

from src.seller.entities.seller import Seller
from src.seller.usecases.manage_seller_usecase import ManageSellerUsecase

# Pruebas para el caso de uso del el manejo de seller, usando un Mock
# para simular el repositorio de Firestore, es decir, en este caso no se utiliza el emulador.


@pytest.fixture
def repository_mock():
    return Mock()


@pytest.fixture
def manage_seller_usecase(repository_mock):
    return ManageSellerUsecase(repository_mock)


class TestManageSellerUsecase:

    def test_get_seller(self, manage_seller_usecase):

        # Definir que el mock del repositorio retorne tres seller.

        mock_sellers = [
            Seller(1, "sport line", "venta de ropa deportiva", "latc", "ec"),
            Seller(2, "troncalnet", "venta de ropa deportiva", "latc", "ec"),
            Seller(3, "sport line", "venta de ropa deportiva", "latc", "ec"),
        ]

        manage_seller_usecase.seller_repository.get_sellers.return_value = mock_sellers

        # Obtener los seller desde el caso de uso, y afirmar que se haya
        # retornado la cantidad correcta de seller.

        sellers = manage_seller_usecase.get_sellers()
        
        assert len(sellers) == len(mock_sellers)

    def test_create_seller(self, manage_seller_usecase):

        # Definir que el mock del repositorio retorne un seller.

        mock_id = 25

        data = {
            "name": "test",
            "short_description": "test",
            "seller_user": "test",
            "address": "test",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        
        mock_seller = Seller.from_dict(data)
        mock_seller.id = mock_id
        
        manage_seller_usecase.seller_repository.create_seller.return_value = mock_seller

        # Crear un seller con el caso de uso.
        
        seller = manage_seller_usecase.create_seller(data)

        # Afirmar que el seller retornado tenga los mismos datos definidos.
        
        assert seller.id == mock_id
        assert seller.name == data["name"]
        assert seller.short_description == data["short_description"]
        assert seller.seller_user == data["seller_user"]
        assert seller.address == data["address"]
