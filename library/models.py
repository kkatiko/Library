from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, validators=[
        MinLengthValidator(2, "Имя должно содержать минимум 2 символа."),
        RegexValidator(r'^[А-Яа-яЁёA-Za-z-]+$', "Имя может содержать только буквы и дефисы.")
    ])
    middle_name = models.CharField(max_length=50, blank=True, validators=[
        RegexValidator(r'^[А-Яа-яЁёA-Za-z-]*$', "Отчество может содержать только буквы и дефисы.")
    ])  # Отчество
    last_name = models.CharField(max_length=50, blank=True, validators=[
        MinLengthValidator(2, "Фамилия должна содержать минимум 2 символа."),
        RegexValidator(r'^[А-Яа-яЁёA-Za-z-]+$', "Фамилия может содержать только буквы и дефисы.")
    ])
    birth_date = models.DateField(null=True, blank=True)
    library_card_number = models.CharField(max_length=20, blank=True, validators=[
        RegexValidator(r'^\d{1,20}$', "Номер читательского билета должен содержать только цифры.")
    ])  # Номер читательского билета
    phone_number = models.CharField(max_length=15, blank=True, validators=[
        RegexValidator(r'^\+?\d{10,15}$', "Телефонный номер должен быть в формате +1234567890 или 1234567890.")
    ])  # Номер телефона

    def __str__(self):
        return self.username

class Library(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    isbn = models.CharField(max_length=13)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    page_count = models.IntegerField(default=0)
    description = models.TextField(default='No description available')
    available_copies = models.IntegerField(default=1)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 


    def __str__(self):
        return self.title

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='loans')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='loans')
    issue_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True) 
    copy_number = models.CharField(max_length=50, blank=True)  

    def __str__(self):
        return f'{self.book.title} - {self.copy_number} (User: {self.user.username})'
    
    class Meta:
        unique_together = ('book', 'user', 'return_date')  # Уникальная пара: книга, пользователь и отсутствие возврата

    def clean(self):
        if Loan.objects.filter(book=self.book, user=self.user, return_date__isnull=True).exists():
            raise ValidationError("Этот пользователь уже забронировал эту книгу.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
