from django.core.management.base import BaseCommand
from tickets.models import Event, Ticket

class Command(BaseCommand):
    help = 'Delete all tickets for a specified event'

    def add_arguments(self, parser):
        parser.add_argument('event_name', type=str, help='The name of the event')

    def handle(self, *args, **kwargs):
        event_name = kwargs['event_name']

        try:
            event = Event.objects.get(name=event_name)
        except Event.DoesNotExist:
            self.stdout.write(self.style.ERROR('Event not found.'))
            return

        tickets_deleted, _ = Ticket.objects.filter(event=event).delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {tickets_deleted} tickets for event "{event.name}".'))