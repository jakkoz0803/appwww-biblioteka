from django.utils import timezone
from .models import Borrow

def update_overdue_borrows():
    Borrow.objects.filter(
        status='borrowed',
        due_date__lt=timezone.now()
    ).update(status='overdue')
