import pytest

from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.books.entities.book import Book
from src.books.repositories.sqlalchemy_books_repository import SQLAlchemyBooksRepository

# Tests para el repositorio de libros usando SQLAlchemy, conectándose
# con el contenedor MySQL corriendo con Docker Compose.

# Contiene las mismas pruebas que el repositorio en Firestore. Ver ese archivo
# para ver una explicación de cómo funcionan los fixtures de Pytest.

@pytest.fixture(scope = "session")
def client():
    return SQLAlchemyClient()

@pytest.fixture(scope = "session")
def repository(client):
    return SQLAlchemyBooksRepository(client, test = True)

@pytest.fixture(autouse = True)
def before_each(repository):
    
    # Limpiar los libros antes de cada prueba, para no afectar los resultados
    # de las pruebas siguientes.

    repository.hard_delete_all_books()
    yield

@pytest.fixture(autouse = True, scope = "session")
def before_and_after_all(client, repository):

    # Crear la tabla antes de todas las pruebas y eliminarla después de todas.

    client.create_tables()
    
    yield
    
    repository.drop_books_table()
    client.dispose_mapper()

class TestSqlAlchemyBooksRepository:

    def test_create_and_get_book(self, repository):

        # Agregar al repositorio un libro nuevo.

        title = "test"
        author = "test"
        pages = 30
        
        book = Book(None, title, author, pages)
        book = repository.create_book(book)

        print("Created book:", book.to_dict())

        # Pedir la instancia del libro recién guardado.

        saved_book = repository.get_book(book.id)

        books = repository.get_books()
        for book in books:
            print(book)

        print(saved_book)
        
        print("Saved book:", saved_book.to_dict())

        # Afirmar que ambos libros sean iguales.

        assert book.id == saved_book.id
        assert book.title == saved_book.title
        assert book.author == saved_book.author
        assert book.pages == saved_book.pages

    def test_delete_book(self, repository):

        # Agregar al repositorio tres libros y guardar sus IDs.

        title = "test"
        author = "test"
        pages = 30

        ids = []

        for i in range(0, 3):
            book = Book(None, title, author, pages)
            book = repository.create_book(book)
            ids.append(book.id)

        print("Added books:", ids)

        # Eliminar el segundo libro del repositorio.

        deleted_id = ids.pop(1)
        print(deleted_id)
        repository.hard_delete_book(deleted_id)

        print("Deleted book:", deleted_id)

        # Obtener las IDs de los libros restantes.

        books = repository.get_books()

        current_ids = []
        for book in books:
            current_ids.append(book.id)

        print("Current books:", current_ids)
        print("Expected books:", ids)

        # Afirmar que las IDs restantes correspondan
        # a los recursos que no fueron eliminados.

        assert set(current_ids) == set(ids)
