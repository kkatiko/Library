from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from library.models import Library, Book, Loan

User = get_user_model()

class CatalogViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.library = Library.objects.create(
            name="Центральная библиотека",
            address="ул. Ленина, д. 5",
            city="Москва",
            postal_code="654321"
        )
        Book.objects.create(
            title="Война и мир",
            author="Лев Толстой",
            publication_year=1869,
            isbn="9781234567890",
            page_count=1225,
            description="Эпическая книга о войне и мире.",
            available_copies=5,
            library=self.library
        )

    def test_catalog_displays_books(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Война и мир")


class FavoritesViewTest(TestCase):

    def setUp(self):
        self.client = Client()
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
        self.client.login(username="testuser", password="password123")

    def test_favorites_accessible_by_authenticated_user(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)

    def test_favorites_not_accessible_by_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('favorites'))
        self.assertNotEqual(response.status_code, 200)


class BookDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user.first_name = "Имя"
        self.user.last_name = "Фамилия"
        self.user.birth_date = "1990-01-01"
        self.user.library_card_number = "12345"
        self.user.phone_number = "+79123456789"
        self.user.save()
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
            library=self.library,
            price=100
        )
        self.client.login(username="testuser", password="password123")

    def test_book_details_displayed(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Евгений Онегин")

    def test_add_to_favorites_button_displayed(self):
        response = self.client.get(reverse('catalog'))
        self.assertContains(response, "В избранное")

    def test_reservation_button_displayed_if_available(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertContains(response, "Зарезервировать")

    def test_purchase_button_displayed(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertContains(response, "Купить за 100")


class LoanReservationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user.first_name = "Имя"
        self.user.last_name = "Фамилия"
        self.user.birth_date = "1990-01-01"
        self.user.library_card_number = "12345"
        self.user.phone_number = "+79123456789"
        self.user.save()
        self.library = Library.objects.create(
            name="Центральная библиотека",
            address="ул. Ленина, д. 5",
            city="Москва",
            postal_code="654321"
        )
        self.book = Book.objects.create(
            title="Преступление и наказание",
            author="Фёдор Достоевский",
            publication_year=1866,
            isbn="9789876543210",
            page_count=500,
            description="Книга о сложных моральных выборах.",
            available_copies=1,
            library=self.library
        )
        self.client.login(username="testuser", password="password123")

    def test_create_loan_on_reservation(self):
        response = self.client.post(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(Loan.objects.count(), 1)

    def test_no_reservation_if_no_copies(self):
        Loan.objects.create(book=self.book, library=self.library, user=self.user)
        response = self.client.post(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(Loan.objects.count(), 1)


class PurchaseTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.library = Library.objects.create(
            name="Центральная библиотека",
            address="ул. Ленина, д. 5",
            city="Москва",
            postal_code="654321"
        )
        self.book = Book.objects.create(
            title="Герой нашего времени",
            author="М.Ю. Лермонтов",
            publication_year=1840,
            isbn="9784433221100",
            page_count=320,
            description="Классический роман о русском характере.",
            available_copies=5,
            library=self.library
        )
        self.client.login(username="testuser", password="password123")

    def test_purchase_page_displayed(self):
        response = self.client.post(reverse('buy_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Спасибо за покупку")
