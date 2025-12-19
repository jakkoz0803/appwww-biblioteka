from django.core.management.base import BaseCommand
from catalog.utils import update_overdue_borrows


class Command(BaseCommand):
    help = "Update overdue borrows"

    def handle(self, *args, **kwargs):
        update_overdue_borrows()
        self.stdout.write(self.style.SUCCESS("Overdue borrows updated"))
