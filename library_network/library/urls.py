from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.profile, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('login/', auth_views.LoginView.as_view(template_name='library/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('add-to-favorites/<int:book_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorites, name='favorites'),
    path('set-library/', views.set_library, name='set_library'),
]
