from rest_framework import serializers
from .models import Genre, Author, Book, Borrow
from django.contrib.auth.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'genre',
            'published_year',
            'is_available',
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id', 'book', 'borrowed_at', 'due_date', 'returned_at']
        read_only_fields = ['borrowed_at', 'returned_at']
