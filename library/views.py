from django.shortcuts import render, redirect, get_object_or_404
from .models import Library, Book, Favorite, Loan
from .forms import ProfileForm, RegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def profile(request):
    libraries = Library.objects.all()
    selected_library_id = request.session.get('selected_library_id')

    # Получаем текущие выдачи книг для пользователя
    current_loans = Loan.objects.filter(user=request.user, return_date__isnull=True)

    if request.method == 'POST':
        # Проверяем, какая форма была отправлена
        if 'library' in request.POST:
            # Логика выбора библиотеки
            selected_library_id = request.POST.get('library')
            request.session['selected_library_id'] = selected_library_id
            return redirect('catalog')
        else:
            # Логика сохранения профиля
            form = ProfileForm(request.POST, instance=request.user, user=request.user)
            if form.is_valid():
                # Проверка заполненности всех полей
                all_fields_filled = all(
                    form.cleaned_data.get(field) for field in form.fields
                )
                if all_fields_filled:
                    form.save()
                    # Устанавливаем флаг после успешного сохранения
                    request.user.save()
                    return redirect('profile')
                else:
                    form.add_error(None, "Все поля должны быть заполнены.")
    else:
        form = ProfileForm(instance=request.user, user=request.user)  # Заполняем форму данными пользователя

    context = {
        'user': request.user,
        'libraries': libraries,
        'selected_library_id': selected_library_id,
        'form': form,  # Передаём форму профиля в шаблон
        'current_loans': current_loans, 
    }
    return render(request, 'library/profile.html', context)



def catalog(request):
    # Получаем выбранную библиотеку
    selected_library_id = request.session.get('selected_library_id')
    
    if selected_library_id:
        books = Book.objects.filter(library_id=selected_library_id)
    else:
        books = Book.objects.all()  

    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('book_id', flat=True)
    else:
        favorites = [] 

    context = {
        'books': books,
        'favorites': favorites,
        'selected_library_id': selected_library_id,  
    }
    return render(request, 'library/catalog.html', context)


def set_library(request):
    if request.method == 'POST':
        selected_library_id = request.POST.get('library')
        request.session['selected_library_id'] = selected_library_id
    return redirect('catalog')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()

    return render(request, 'library/register.html', {'form': form})


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
    issued_count = Loan.objects.filter(book=book, return_date__isnull=True).count()
    available_copies = book.available_copies - issued_count

    user = request.user
    required_fields = ['first_name', 'last_name', 'birth_date', 'library_card_number', 'phone_number']
    missing_fields = [field for field in required_fields if not getattr(user, field)]

    # Проверка, что профиль заполнен
    if missing_fields:
        return render(request, 'library/book_detail.html', {
            'book': book,
            'is_favorite': is_favorite,
            'available_copies': available_copies,
            'is_book_available': available_copies > 0,
            'missing_fields': missing_fields,
        })

    # Проверка, что пользователь уже зарезервировал эту книгу
    if Loan.objects.filter(book=book, user=request.user, return_date__isnull=True).exists():
        context = {
            'book': book,
            'is_favorite': is_favorite,
            'available_copies': available_copies,
            'is_book_available': available_copies > 0,
            'error_message': "You have already reserved this book. Return it before reserving again.",
        }
        return render(request, 'library/book_detail.html', context)

    if request.method == 'POST':
        if available_copies > 0:
            Loan.objects.create(book=book, library=book.library, user=request.user)
            return redirect('book_detail', book_id=book_id)

    context = {
        'book': book,
        'is_favorite': is_favorite,
        'available_copies': available_copies,
        'is_book_available': available_copies > 0,
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

@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        # Логика имитации покупки
        # Здесь можно добавить запись в историю покупок, отправку уведомлений и т.д.
        return render(request, 'library/buy_success.html', {'book': book})
    return redirect('book_detail', book_id=book_id)
