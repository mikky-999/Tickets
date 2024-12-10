from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tickets.models import Event, Ticket
import uuid

class Command(BaseCommand):
    help = 'Create a specified number of tickets for a particular event and user'

    def add_arguments(self, parser):
        parser.add_argument('event_name', type=str, help='The name of the event')
        parser.add_argument('username', type=str, help='The username of the user')
        parser.add_argument('num_tickets', type=int, help='The number of tickets to create')

    def handle(self, *args, **kwargs):
        event_name = kwargs['event_name']
        username = kwargs['username']
        num_tickets = kwargs['num_tickets']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found.'))
            return

        try:
            event = Event.objects.get(name=event_name, user=user)
        except Event.DoesNotExist:
            self.stdout.write(self.style.ERROR('Event not found for the given user.'))
            return

        tickets = []
        for _ in range(num_tickets):
            ticket = Ticket(
                code=uuid.uuid4(),
                event=event,
                is_used=False
            )
            tickets.append(ticket)

        Ticket.objects.bulk_create(tickets)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_tickets} tickets for event "{event.name}" created by user "{user.username}".'))