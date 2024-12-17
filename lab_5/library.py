class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author})"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        """Добавление книги в библиотеку."""
        if not isinstance(book, Book):
            raise ValueError("Должен быть объект класса Book.")
        self.books.append(book)

    def remove_book(self, book):
        """Удаление книги из библиотеки."""
        if book not in self.books:
            raise ValueError("Книга не найдена в библиотеке.")
        self.books.remove(book)

    def find_books_by_author(self, author):
        """Поиск книг по автору."""
        return [book for book in self.books if book.author == author]

    def get_all_books(self):
        """Возвращает все книги в библиотеке."""
        return self.books

    def clear_library(self):
        """Очищает библиотеку."""
        self.books.clear()