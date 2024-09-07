from django.core.management.base import BaseCommand
from main.views import backup_now  # Reuse the existing backup function
from django.http import HttpRequest

class Command(BaseCommand):
    help = 'Backup the database'

    def handle(self, *args, **kwargs):
        request = HttpRequest()
        backup_now(request)
        self.stdout.write(self.style.SUCCESS('Database backup completed'))