import pytest

from datetime import datetime
from unittest.mock import Mock

from src.product.entities.product import Product
from src.product.usecases.manage_product_usecase import ManageProductUsecase

# Pruebas para el caso de uso del el manejo de product, usando un Mock
# para simular el repositorio de Firestore, es decir, en este caso no se utiliza el emulador.


@pytest.fixture
def repository_mock():
    return Mock()


@pytest.fixture
def manage_product_usecase(repository_mock):
    return ManageProductUsecase(repository_mock)


class TestManageProductUsecase:

    def test_get_product(self, manage_product_usecase):

        # Definir que el mock del repositorio retorne tres product.

        mock_products = [
            Product(1, "sport line", "venta de ropa deportiva", 12, 1),
            Product(2, "troncalnet", "venta de ropa deportiva", 13, 2),
            Product(3, "sport line", "venta de ropa deportiva", 14, 3),
        ]

        manage_product_usecase.product_repository.get_products.return_value = mock_products

        # Obtener los product desde el caso de uso, y afirmar que se haya
        # retornado la cantidad correcta de product.

        products = manage_product_usecase.get_products()
        
        assert len(products) == len(mock_products)

    def test_create_product(self, manage_product_usecase):

        # Definir que el mock del repositorio retorne un product.

        mock_id = 25

        data = {
            "name": "test",
            "short_description": "test",
            "quantity": 12,
            "seller_id": 13,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        
        mock_product = Product.from_dict(data)
        mock_product.id = mock_id
        
        manage_product_usecase.product_repository.create_product.return_value = mock_product

        # Crear un product con el caso de uso.
        
        product = manage_product_usecase.create_product(data)

        # Afirmar que el product retornado tenga los mismos datos definidos.
        
        assert product.id == mock_id
        assert product.name == data["name"]
        assert product.short_description == data["short_description"]
        assert product.quantity == data["quantity"]
        assert product.seller_id == data["seller_id"]
