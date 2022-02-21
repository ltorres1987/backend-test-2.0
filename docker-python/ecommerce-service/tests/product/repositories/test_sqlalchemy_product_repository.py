import pytest

from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.product.entities.product import Product
from src.product.repositories.sqlalchemy_product_repository import SQLAlchemyProductRepository

# Tests para el repositorio de product usando SQLAlchemy, conectándose
# con el contenedor MySQL corriendo con Docker Compose.

# Contiene las mismas pruebas que el repositorio en Firestore. Ver ese archivo
# para ver una explicación de cómo funcionan los fixtures de Pytest.


@pytest.fixture(scope="session")
def client():
    return SQLAlchemyClient()


@pytest.fixture(scope="session")
def repository(client):
    return SQLAlchemyProductRepository(client, test=True)


@pytest.fixture(autouse=True)
def before_each(repository):
    
    # Limpiar los product antes de cada prueba, para no afectar los resultados
    # de las pruebas siguientes.

    repository.hard_delete_all_product()
    yield


@pytest.fixture(autouse=True, scope="session")
def before_and_after_all(client, repository):

    # Crear la tabla antes de todas las pruebas y eliminarla después de todas.

    client.create_tables()
    
    yield
    
    repository.drop_product_table()
    client.dispose_mapper()


class TestSqlAlchemyProductRepository:

    def test_create_and_get_product(self, repository):

        # Agregar al repositorio un product nuevo.

        id = "1"
        name = "test"
        short_description = "test"
        quantity = 12
        seller_id = 13
        
        product = Product(None, name, short_description, quantity, seller_id)
        product = repository.create_product(product)

        print("Created product:", product.to_dict())

        # Pedir la instancia del product recién guardado.

        saved_product = repository.get_product(product.id)

        products = repository.get_products()
        for product in products:
            print(product)

        print(saved_product)
        
        print("Saved product:", saved_product.to_dict())

        # Afirmar que ambos product sean iguales.

        assert product.id == saved_product.id
        assert product.name == saved_product.name
        assert product.short_description == saved_product.short_description
        assert product.quantity == saved_product.quantity
        assert product.seller_id == saved_product.seller_id

    def test_delete_product(self, repository):

        # Agregar al repositorio tres product y guardar sus IDs.

        name = "test"
        short_description = "test"
        quantity = 12
        seller_id = 13

        ids = []

        for i in range(0, 3):
            product = Product(None, name, short_description, quantity, seller_id)
            product = repository.create_product(product)
            ids.append(product.id)

        print("Added product:", ids)

        # Eliminar el segundo product del repositorio.

        deleted_id = ids.pop(1)
        print(deleted_id)
        repository.hard_delete_product(deleted_id)

        print("Deleted product:", deleted_id)

        # Obtener las IDs de los product restantes.

        products = repository.get_products()

        current_ids = []
        for product in products:
            current_ids.append(product.id)

        print("Current product:", current_ids)
        print("Expected product:", ids)

        # Afirmar que las IDs restantes correspondan
        # a los recursos que no fueron eliminados.

        assert set(current_ids) == set(ids)
