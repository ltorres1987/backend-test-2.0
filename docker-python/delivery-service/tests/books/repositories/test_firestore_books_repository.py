import pytest

from src.frameworks.db.firestore import create_firestore_client
from src.books.entities.book import Book
from src.books.repositories.firestore_books_repository import FirestoreBooksRepository

# Tests para el repositorio de libros en Firestore.
# Se conecta con el emulador para realizar las llamadas.

# Los fixtures sirven para definir funciones que son llamadas automáticamente en cada prueba si es que sus
# métodos las reciben como parámetros, evitando la repetición de código. Por ejemplo, si una prueba recibe
# como parámetro "repository", entonces Pytest automáticamente llamará al fixture "repository", pasando su
# valor de retorno al método.

# Si un fixture tiene la opción "scope" equivalente a "class", entonces ese fixture sólo se ejecutará una
# vez durante todas las pruebas de la clase, reusando el mismo valor de retorno. Si no se define "scope",
# entonces es llamado para cada una de las pruebas de la clase.

# Si un fixture tiene la opción "autouse" como True, entonces la función será ejecutada automáticamente
# por cada prueba sin tener que definir el parámetro explícitamente, útil para agregar instrucciones
# antes y después de cada prueba. La palabra "yield" significa realizar la ejecución misma de la prueba.

@pytest.fixture(scope = "class")
def client():
    return create_firestore_client()

@pytest.fixture(scope = "class")
def repository(client):
    return FirestoreBooksRepository(client, test = True)

@pytest.fixture(autouse = True)
def before_each(repository):
    
    # Limpiar los libros antes de cada prueba, para no afectar los resultados
    # de las pruebas siguientes.

    repository.hard_delete_all_books()
    yield

@pytest.fixture(autouse = True, scope = "class")
def after_all(repository):

    # Limpiar los libros después de todas las pruebas.

    yield
    repository.hard_delete_all_books()

class TestFirestoreBooksRepository:

    def test_create_and_get_book(self, repository):

        # Agregar al repositorio un libro nuevo.

        data = {
            "title": "test",
            "author": "test",
            "pages": 30,
        }
        
        book = Book.from_dict(data)
        book = repository.create_book(book)

        print("Created book:", book.to_dict())

        # Pedir la instancia del libro recién guardado.

        saved_book = repository.get_book(book.id)
        print("Saved book:", saved_book.to_dict())

        # Afirmar que ambos libros sean iguales.

        assert book.id == saved_book.id
        assert book.title == saved_book.title
        assert book.author == saved_book.author
        assert book.pages == saved_book.pages

    def test_delete_book(self, repository):

        # Agregar al repositorio tres libros y guardar sus IDs.

        data = {
            "title": "test",
            "author": "test",
            "pages": 30,
        }

        ids = []

        for i in range(0, 3):
            book = Book.from_dict(data)
            book = repository.create_book(book)
            ids.append(book.id)

        print("Added books:", ids)

        # Eliminar el segundo libro del repositorio.

        deleted_id = ids.pop(1)
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
