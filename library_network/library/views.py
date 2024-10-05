from django.shortcuts import render, redirect, get_object_or_404
from .models import Library, Book, Favorite, Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def profile(request):
    libraries = Library.objects.all()

    if request.method == 'POST':
        selected_library_id = request.POST.get('library')
        request.session['selected_library_id'] = selected_library_id  # Сохраняем выбранную библиотеку в сессии
        return redirect('catalog')

    context = {
        'user': request.user,
        'libraries': libraries,
        'selected_library_id': request.session.get('selected_library_id'),
    }
    return render(request, 'library/profile.html', context)

def catalog(request):
    # Получаем выбранную библиотеку
    selected_library_id = request.session.get('selected_library_id')
    
    if selected_library_id:
        books = Book.objects.filter(library_id=selected_library_id)
    else:
        books = Book.objects.all()  # Если библиотека не выбрана, показываем все книги

    # Проверка авторизации пользователя для избранного
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('book_id', flat=True)
    else:
        favorites = []  # Пустой список для неавторизованных пользователей

    context = {
        'books': books,
        'favorites': favorites,
        'selected_library_id': selected_library_id,  # Добавляем информацию о выбранной библиотеке
    }
    return render(request, 'library/catalog.html', context)

def set_library(request):
    if request.method == 'POST':
        selected_library_id = request.POST.get('library')
        request.session['selected_library_id'] = selected_library_id
    return redirect('catalog')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'library/register.html', {'form': form})

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
    reserved_count = Reservation.objects.filter(book=book).count()  # Забронированные книги

    if request.method == 'POST':
        if reserved_count < book.available_copies:  # Проверяем, есть ли доступные экземпляры
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            purpose = request.POST.get('purpose')
            Reservation.objects.create(book=book, user=request.user, name=name, surname=surname, purpose=purpose)
            return redirect('book_detail', book_id=book_id)

    is_book_available = reserved_count < book.available_copies
    available_copies = book.available_copies - reserved_count  # Вычисляем доступные экземпляры

    context = {
        'book': book,
        'is_favorite': is_favorite,
        'is_book_available': is_book_available,
        'available_copies': available_copies,  # Передаем в шаблон
    }
    return render(request, 'library/book_detail.html', context)


@login_required
def add_to_favorites(request, book_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        book = get_object_or_404(Book, id=book_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
        
        if created:
            return JsonResponse({'status': 'added'})
        else:
            favorite.delete()
            return JsonResponse({'status': 'removed'})
    else:
        return JsonResponse({'status': 'error'}, status=400)
    
@login_required
def favorites(request):
    favorite_books = Favorite.objects.filter(user=request.user)
    context = {
        'favorite_books': favorite_books
    }
    return render(request, 'library/favorites.html', context)
