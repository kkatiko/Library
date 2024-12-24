from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Library, Book, CustomUser, Loan

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('middle_name', 'birth_date', 'library_card_number', 'phone_number')}),
    )

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'copy_number', 'user', 'issue_date', 'return_date')
    readonly_fields = ('issue_date', 'copy_number')
    list_filter = ('book', 'library', 'user', 'issue_date', 'return_date')

admin.site.register(Library)
admin.site.register(Book)
