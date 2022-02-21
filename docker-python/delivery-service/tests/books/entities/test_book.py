from datetime import datetime

from src.books.entities.book import Book

class TestBook:

    def test_to_dict(self):

        # Crear instancia del libro.

        id = "1"
        title = "test"
        author = "test"
        pages = 20

        book = Book(id, title, author, pages)

        # Obtener diccionario y afirmar que sean iguales los datos.

        dict = book.to_dict()

        assert dict["id"] == id
        assert dict["title"] == title
        assert dict["author"] == author
        assert dict["pages"] == pages

    def test_serialize(self):

        # Crear instancia del libro con fechas.

        id = "1"
        title = "test"
        author = "test"
        pages = 20
        created_at = datetime(year = 2021, month = 12, day = 25, hour = 10, minute = 24, second = 13, microsecond = 321654)
        updated_at = datetime(year = 2021, month = 12, day = 25, hour = 10, minute = 24, second = 14, microsecond = 321654)
        deleted_at = datetime(year = 2021, month = 12, day = 25, hour = 10, minute = 24, second = 15, microsecond = 321654)

        book = Book(id, title, author, pages, created_at, updated_at, deleted_at)

        # Obtener diccionario serializable y afirmar que sean iguales los datos,
        # que las fechas vengan formateadas y que no venga con fecha de borrado.

        data = book.serialize()

        assert data["id"] == id
        assert data["title"] == title
        assert data["author"] == author
        assert data["pages"] == pages
        assert data["created_at"] == "2021-12-25 10:24:13"
        assert data["updated_at"] == "2021-12-25 10:24:14"
        assert "deleted_at" not in data

    def test_from_dict(self):

        # Crear diccionario de datos.

        dict = {
            "id": "2",
            "title": "test",
            "author": "test",
            "pages": 30,
        }

        # Obtener instancia desde diccionario y afirmar que sean iguales los datos.

        book = Book.from_dict(dict)

        assert book.id == dict["id"]
        assert book.title == dict["title"]
        assert book.author == dict["author"]
        assert book.pages == dict["pages"]