from django.db import models
from django.contrib.auth.models import User

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
    
    # Добавляем связь с библиотекой (ForeignKey)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Имя бронирующего
    surname = models.CharField(max_length=100)  # Фамилия бронирующего
    purpose = models.TextField()  # Цель бронирования
    reservation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.surname} - {self.book.title}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'

