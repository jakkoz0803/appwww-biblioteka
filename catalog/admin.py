from django.contrib import admin
from .models import Genre, Author, Book, Borrow

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'is_available']
    list_filter = ['genre', 'is_available']
    search_fields = ['title', 'author__last_name']

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'returned_at', 'due_date')
    list_filter = ('borrowed_at', 'returned_at')