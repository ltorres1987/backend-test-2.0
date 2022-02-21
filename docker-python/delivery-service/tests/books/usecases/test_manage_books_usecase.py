import pytest

from datetime import datetime
from unittest.mock import Mock

from src.books.entities.book import Book
from src.books.usecases.manage_books_usecase import ManageBooksUsecase

# Pruebas para el caso de uso del el manejo de libros, usando un Mock
# para simular el repositorio de Firestore, es decir, en este caso no se utiliza el emulador.

@pytest.fixture
def repository_mock():
    return Mock()

@pytest.fixture
def manage_books_usecase(repository_mock):
    return ManageBooksUsecase(repository_mock)

class TestManageBooksUsecase:

    def test_get_books(self, manage_books_usecase):

        # Definir que el mock del repositorio retorne tres libros.

        mock_books = [
            Book(1, "Book1", "Author1", 10),
            Book(2, "Book2", "Author2", 20),
            Book(3, "Book3", "Author3", 30),
        ]

        manage_books_usecase.books_repository.get_books.return_value = mock_books

        # Obtener los libros desde el caso de uso, y afirmar que se haya
        # retornado la cantidad correcta de libros.

        books = manage_books_usecase.get_books()
        
        assert len(books) == len(mock_books)

    def test_create_book(self, manage_books_usecase):

        # Definir que el mock del repositorio retorne un libro.

        mock_id = 25

        data = {
            "title": "test-title",
            "author": "test-author",
            "pages": 40,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        };
        
        mock_book = Book.from_dict(data)
        mock_book.id = mock_id
        
        manage_books_usecase.books_repository.create_book.return_value = mock_book

        # Crear un libro con el caso de uso.
        
        book = manage_books_usecase.create_book(data);

        # Afirmar que el libro retornado tenga los mismos datos definidos.
        
        assert book.id == mock_id
        assert book.title == data["title"]
        assert book.author == data["author"]
        assert book.pages == data["pages"]