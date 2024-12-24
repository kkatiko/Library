from django.test import TestCase
from django.contrib.auth import get_user_model
from library.models import Library, Book, Favorite, Loan
from django.core.exceptions import ValidationError

User = get_user_model()

class LibraryModelTest(TestCase):

    def test_create_library(self):
        library = Library.objects.create(
            name="Центральная библиотека",
            address="ул. Пушкина, д. 10",
            city="Москва",
            postal_code="123456"
        )
        self.assertEqual(Library.objects.count(), 1)
        self.assertEqual(str(library), "Центральная библиотека")


class BookModelTest(TestCase):

    def setUp(self):
        self.library = Library.objects.create(
            name="Центральная библиотека",
            address="ул. Ленина, д. 5",
            city="Москва",
            postal_code="654321"
        )

    def test_create_book(self):
        book = Book.objects.create(
            title="Война и мир",
            author="Лев Толстой",
            publication_year=1869,
            isbn="9781234567890",
            page_count=1225,
            description="Эпическая книга о войне и мире.",
            available_copies=5,
            library=self.library
        )
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(str(book), "Война и мир")

    def test_decrease_available_copies(self):
        book = Book.objects.create(
            title="Преступление и наказание",
            author="Фёдор Достоевский",
            publication_year=1866,
            isbn="9789876543210",
            page_count=500,
            description="Книга о сложных моральных выборах.",
            available_copies=3,
            library=self.library
        )
        Loan.objects.create(book=book, library=self.library, user=self.create_user())
        book.refresh_from_db()
        self.assertEqual(book.available_copies, 3)  # Доступные копии не изменяются при бронировании

    def create_user(self):
        return User.objects.create_user(username="testuser", password="password123")


class FavoriteModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.library = Library.objects.create(
            name="Центральная библиотека",
            address="ул. Ленина, д. 5",
            city="Москва",
            postal_code="654321"
        )
        self.book = Book.objects.create(
            title="Анна Каренина",
            author="Лев Толстой",
            publication_year=1877,
            isbn="9781122334455",
            page_count=864,
            description="Трагическая история любви.",
            available_copies=5,
            library=self.library
        )

    def test_add_to_favorites(self):
        favorite = Favorite.objects.create(user=self.user, book=self.book)
        self.assertEqual(Favorite.objects.count(), 1)
        self.assertEqual(str(favorite), "testuser - Анна Каренина")

    def test_remove_from_favorites(self):
        favorite = Favorite.objects.create(user=self.user, book=self.book)
        favorite.delete()
        self.assertEqual(Favorite.objects.count(), 0)


class LoanModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.library = Library.objects.create(
            name="Центральная библиотека",
            address="ул. Ленина, д. 5",
            city="Москва",
            postal_code="654321"
        )
        self.book = Book.objects.create(
            title="Евгений Онегин",
            author="Александр Пушкин",
            publication_year=1833,
            isbn="9789988776655",
            page_count=224,
            description="Классический роман в стихах.",
            available_copies=2,
            library=self.library
        )

    def test_create_loan(self):
        loan = Loan.objects.create(book=self.book, library=self.library, user=self.user)
        self.assertEqual(Loan.objects.count(), 1)
        self.assertEqual(str(loan), f"Евгений Онегин - {loan.copy_number} (User: testuser)")

    def test_unique_loan_per_user(self):
        Loan.objects.create(book=self.book, library=self.library, user=self.user)
        with self.assertRaisesMessage(ValidationError, "Этот пользователь уже забронировал эту книгу."):
            Loan.objects.create(book=self.book, library=self.library, user=self.user)

