import pytest

from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.seller.entities.seller import Seller
from src.seller.repositories.sqlalchemy_seller_repository import SQLAlchemySellerRepository

# Tests para el repositorio de seller usando SQLAlchemy, conectándose
# con el contenedor MySQL corriendo con Docker Compose.

# Contiene las mismas pruebas que el repositorio en Firestore. Ver ese archivo
# para ver una explicación de cómo funcionan los fixtures de Pytest.


@pytest.fixture(scope="session")
def client():
    return SQLAlchemyClient()


@pytest.fixture(scope="session")
def repository(client):
    return SQLAlchemySellerRepository(client, test=True)


@pytest.fixture(autouse=True)
def before_each(repository):
    
    # Limpiar los seller antes de cada prueba, para no afectar los resultados
    # de las pruebas siguientes.

    repository.hard_delete_all_seller()
    yield


@pytest.fixture(autouse=True, scope="session")
def before_and_after_all(client, repository):

    # Crear la tabla antes de todas las pruebas y eliminarla después de todas.

    client.create_tables()
    
    yield
    
    repository.drop_seller_table()
    client.dispose_mapper()


class TestSqlAlchemySellerRepository:

    def test_create_and_get_seller(self, repository):

        # Agregar al repositorio un seller nuevo.

        id = "1"
        name = "test"
        short_description = "test"
        seller_user = "test"
        address = "test"
        
        seller = Seller(None, name, short_description, seller_user, address)
        seller = repository.create_seller(seller)

        print("Created seller:", seller.to_dict())

        # Pedir la instancia del seller recién guardado.

        saved_seller = repository.get_seller(seller.id)

        sellers = repository.get_sellers()
        for seller in sellers:
            print(seller)

        print(saved_seller)
        
        print("Saved seller:", saved_seller.to_dict())

        # Afirmar que ambos seller sean iguales.

        assert seller.id == saved_seller.id
        assert seller.name == saved_seller.name
        assert seller.short_description == saved_seller.short_description
        assert seller.seller_user == saved_seller.seller_user
        assert seller.address == saved_seller.address

    def test_delete_seller(self, repository):

        # Agregar al repositorio tres seller y guardar sus IDs.

        name = "test"
        short_description = "test"
        seller_user = "test"
        address = "test"

        ids = []

        for i in range(0, 3):
            seller = Seller(None, name, short_description, seller_user, address)
            seller = repository.create_seller(seller)
            ids.append(seller.id)

        print("Added sellers:", ids)

        # Eliminar el segundo seller del repositorio.

        deleted_id = ids.pop(1)
        print(deleted_id)
        repository.hard_delete_seller(deleted_id)

        print("Deleted seller:", deleted_id)

        # Obtener las IDs de los seller restantes.

        sellers = repository.get_sellers()

        current_ids = []
        for seller in sellers:
            current_ids.append(seller.id)

        print("Current seller:", current_ids)
        print("Expected seller:", ids)

        # Afirmar que las IDs restantes correspondan
        # a los recursos que no fueron eliminados.

        assert set(current_ids) == set(ids)
