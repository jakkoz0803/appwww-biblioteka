from django.db import models
from django.conf import settings
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
    )
    published_year = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Borrow(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),   # wypozyczona
        ('returned', 'Returned'),   # zwrocona
        ('overdue', 'Overdue'),     # termin zwrotu minal
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='borrows'
    )

    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='borrows'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='borrowed'
    )

    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField()

    class Meta:
        permissions = [
            ("can_view_all_borrows", "Can view all borrows"),
        ]

    def mark_returned(self):
        self.status = 'returned'
        self.returned_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user} → {self.book} ({self.status})"