from django.urls import path
from . import api_views

urlpatterns = [
    path('genres/', api_views.genre_list),
    path('authors/', api_views.author_list),
    path('books/', api_views.book_list),
    path('auth/register/', api_views.register_user),
    path('borrows/', api_views.borrow_list),
    path('borrows/create/', api_views.borrow_create),
    path('borrows/my/', api_views.my_borrows),
    path('borrows/<int:pk>/return/', api_views.return_book),
]
