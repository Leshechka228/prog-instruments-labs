import pytest
from library import Book, Library
from unittest.mock import MagicMock


@pytest.fixture
def library():
    """Фикстура для создания экземпляра библиотеки."""
    return Library()


def test_add_book(library):
    """Тест добавления книги в библиотеку."""
    book = Book("1984", "George Orwell")
    library.add_book(book)
    assert len(library.get_all_books()) == 1
    assert library.get_all_books()[0] == book


def test_remove_book(library):
    """Тест удаления книги из библиотеки."""
    book = Book("The Hobbit", "J.R.R. Tolkien")
    library.add_book(book)
    library.remove_book(book)
    assert len(library.get_all_books()) == 0


def test_remove_nonexistent_book(library):
    """Тест удаления несуществующей книги."""
    book = Book("Unexisting Book", "Unknown")
    with pytest.raises(ValueError, match="Книга не найдена в библиотеке."):
        library.remove_book(book)


def test_find_books_by_author(library):
    """Тест поиска книг по автору."""
    book1 = Book("1984", "George Orwell")
    book2 = Book("Animal Farm", "George Orwell")
    book3 = Book("The Hobbit", "J.R.R. Tolkien")
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    result = library.find_books_by_author("George Orwell")
    assert len(result) == 2
    assert book1 in result
    assert book2 in result


@pytest.mark.parametrize("title, author", [
    ("Brave New World", "Aldous Huxley"),
    ("Fahrenheit 451", "Ray Bradbury"),
])
def test_add_multiple_books(library, title, author):
    """Параметризованный тест для добавления нескольких книг."""
    book = Book(title, author)
    library.add_book(book)
    assert len(library.get_all_books()) == 1
    assert library.get_all_books()[0] == book


def test_clear_library(library):
    """Тест очистки библиотеки."""
    library.add_book(Book("1984", "George Orwell"))
    library.clear_library()
    assert len(library.get_all_books()) == 0


def test_library_mock(library):
    """Тест с использованием моков."""
    mocked_book = MagicMock(spec=Book)
    library.add_book(mocked_book)

    assert mocked_book in library.get_all_books()
    library.remove_book(mocked_book)
    assert len(library.get_all_books()) == 0
