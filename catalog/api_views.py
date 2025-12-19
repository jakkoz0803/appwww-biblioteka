from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from .models import Genre, Author, Book, Borrow
from .serializers import GenreSerializer, AuthorSerializer, BookSerializer, RegisterSerializer, BorrowSerializer
from .utils import update_overdue_borrows

@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def author_list(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def borrow_book(request):
    update_overdue_borrows()

    book_id = request.data.get('book')

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

    if Borrow.objects.filter(book=book, status='borrowed').exists():
        return Response({'error': 'Book already borrowed'}, status=400)

    borrow = Borrow.objects.create(
        user=request.user,
        book=book,
        due_date=timezone.now() + timezone.timedelta(days=14)
    )

    serializer = BorrowSerializer(borrow)
    return Response(serializer.data, status=201)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_borrows(request):
    update_overdue_borrows()

    borrows = Borrow.objects.filter(user=request.user)
    serializer = BorrowSerializer(borrows, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def borrow_create(request):
    update_overdue_borrows()

    serializer = BorrowSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    book = serializer.validated_data['book']

    if not book.is_available:
        return Response(
            {"detail": "This book is currently unavailable."},
            status=status.HTTP_400_BAD_REQUEST
        )

    borrow = serializer.save(user=request.user)

    book.is_available = False
    book.save()

    return Response(BorrowSerializer(borrow).data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, DjangoModelPermissions])
def borrow_list(request):
    update_overdue_borrows()

    borrows = Borrow.objects.all()
    serializer = BorrowSerializer(borrows, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def return_book(request, pk):
    try:
        borrow = Borrow.objects.get(pk=pk)
    except Borrow.DoesNotExist:
        return Response(
            {"detail": "Borrow not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if borrow.user != request.user:
        return Response(
            {"detail": "You cannot return someone else's book"},
            status=status.HTTP_403_FORBIDDEN
        )

    if borrow.status == 'returned':
        return Response(
            {"detail": "Book already returned"},
            status=status.HTTP_400_BAD_REQUEST
        )

    borrow.status = 'returned'
    borrow.returned_at = timezone.now()
    borrow.save()

    book = borrow.book
    book.is_available = True
    book.save()

    return Response(
        {"detail": "Book returned successfully"},
        status=status.HTTP_200_OK
    )
