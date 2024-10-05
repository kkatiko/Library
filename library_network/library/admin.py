from django.contrib import admin
from .models import Library, Book, Favorite

admin.site.register(Library)
admin.site.register(Book)
admin.site.register(Favorite)