from django.test import TestCase
from library.forms import RegistrationForm, ProfileForm
from django.contrib.auth import get_user_model

User = get_user_model()


class FormValidationTests(TestCase):

    def test_registration_form_valid(self):
        form_data = {
            'username': 'newuser',
            'password1': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'password1': 'SecurePassword123!',
            'password2': 'DifferentPassword123!',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_registration_form_username_uniqueness(self):
        User.objects.create_user(username='newuser', password='password123')
        form_data = {
            'username': 'newuser',
            'password1': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_profile_form_valid(self):
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'birth_date': '01.01.1990',
            'library_card_number': '1234567890',
            'phone_number': '+71234567890',
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_form_invalid_phone_number(self):
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'birth_date': '01.01.1990',
            'library_card_number': '1234567890',
            'phone_number': '12345',  # Invalid phone number
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_profile_form_invalid_birth_date(self):
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'birth_date': '01.01.2050',  # Birthdate in the future
            'library_card_number': '1234567890',
            'phone_number': '+71234567890',
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)
