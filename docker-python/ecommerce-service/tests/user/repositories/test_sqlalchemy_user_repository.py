import pytest

from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.user.entities.user import User
from src.user.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository

# Tests para el repositorio de user usando SQLAlchemy, conectándose
# con el contenedor MySQL corriendo con Docker Compose.

# Contiene las mismas pruebas que el repositorio en Firestore. Ver ese archivo
# para ver una explicación de cómo funcionan los fixtures de Pytest.


@pytest.fixture(scope="session")
def client():
    return SQLAlchemyClient()


@pytest.fixture(scope="session")
def repository(client):
    return SQLAlchemyUserRepository(client, test=True)


@pytest.fixture(autouse=True)
def before_each(repository):
    
    # Limpiar los user antes de cada prueba, para no afectar los resultados
    # de las pruebas siguientes.

    repository.hard_delete_all_user()
    yield


@pytest.fixture(autouse=True, scope="session")
def before_and_after_all(client, repository):

    # Crear la tabla antes de todas las pruebas y eliminarla después de todas.

    client.create_tables()
    
    yield
    
    repository.drop_user_table()
    client.dispose_mapper()


class TestSqlAlchemyUserRepository:

    def test_create_and_get_user(self, repository):

        # Agregar al repositorio un user nuevo.

        id = "1"
        name = "test"
        email = "test"
        city = "test"
        address = "test"
        
        user = User(None, name, email, city, address)
        user = repository.create_user(user)

        print("Created user:", user.to_dict())

        # Pedir la instancia del user recién guardado.

        saved_user = repository.get_user(user.id)

        users = repository.get_users()
        for user in users:
            print(user)

        print(saved_user)
        
        print("Saved user:", saved_user.to_dict())

        # Afirmar que ambos user sean iguales.

        assert user.id == saved_user.id
        assert user.name == saved_user.name
        assert user.email == saved_user.email
        assert user.city == saved_user.city
        assert user.address == saved_user.address

    def test_delete_user(self, repository):

        # Agregar al repositorio tres user y guardar sus IDs.

        name = "test"
        email = "test"
        city = "test"
        address = "test"

        ids = []

        for i in range(0, 3):
            user = User(None, name, email, city, address)
            user = repository.create_user(user)
            ids.append(user.id)

        print("Added users:", ids)

        # Eliminar el segundo user del repositorio.

        deleted_id = ids.pop(1)
        print(deleted_id)
        repository.hard_delete_user(deleted_id)

        print("Deleted user:", deleted_id)

        # Obtener las IDs de los user restantes.

        users = repository.get_users()

        current_ids = []
        for user in users:
            current_ids.append(user.id)

        print("Current user:", current_ids)
        print("Expected user:", ids)

        # Afirmar que las IDs restantes correspondan
        # a los recursos que no fueron eliminados.

        assert set(current_ids) == set(ids)
