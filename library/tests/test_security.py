from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model  # Добавляем импорт модели пользователя
from library.models import Library, Book, Loan

User = get_user_model()  # Определяем User как модель пользователя

class SecurityTests(TestCase):

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
            title="Мёртвые души",
            author="Н.В. Гоголь",
            publication_year=1842,
            isbn="9781239876543",
            page_count=352,
            description="Сатирический роман о жизни русского общества.",
            available_copies=3,
            library=self.library
        )

    def test_favorites_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse('favorites'))
        self.assertNotEqual(response.status_code, 200)

    def test_reservation_requires_profile_completion(self):
        self.user.library_card_number = ""
        self.user.save()
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse('book_detail', args=[self.book.id]), data={})
        self.assertEqual(Loan.objects.count(), 0)

    def test_admin_not_accessible_to_regular_users(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('admin:index'))
        self.assertNotEqual(response.status_code, 200)
