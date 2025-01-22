from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.management import call_command

class Command(BaseCommand):
    help = "Load fixtures in a transactional way"

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():  # Start a transaction
                # Load fixtures in the required order

                
                self.stdout.write("Loading events...")
                call_command('loaddata', 'events.json')

                self.stdout.write("Loading event comments...")
                call_command('loaddata', 'event_comments.json')
                
                self.stdout.write("Loading templates...")
                call_command('loaddata', 'templates.json')

                self.stdout.write("Loading custom fields...")
                call_command('loaddata', 'custom_fields.json',verbosity=3)

                self.stdout.write(self.style.SUCCESS("All fixtures loaded successfully!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error occurred: {e}"))
            # Rollback will occur automatically due to transaction.atomic
