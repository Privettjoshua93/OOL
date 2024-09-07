from django.core.management.base import BaseCommand
from main.views import backup_now  # Reuse the existing backup function

class Command(BaseCommand):
    help = 'Backup the database'

    def handle(self, *args, **kwargs):
        backup_now()  # Call backup_now directly without HttpRequest object
        self.stdout.write(self.style.SUCCESS('Database backup completed'))