from django.shortcuts import render, redirect
import uuid
from .models import Ticket
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def scanning(request):
    return render(request, 'tickets/scan_ticket.html')

@login_required
def valid(request):
    return render(request, 'tickets/valid_ticket.html')

@login_required
def invalid(request):
    return render(request, 'tickets/invalid_ticket.html')

@login_required
def scanned(request):
    return render(request, 'tickets/already_scanned.html')

@login_required
def validate_ticket(request):
    code = request.POST.get('code')
    print(f"Received code: {code}")
    
    # Check if the code is a valid UUID format
    try:
        uuid.UUID(str(code))  # Attempt to convert the code to a UUID
    except ValueError:
        # If the code is not a valid UUID, it's an invalid QR code
        print("Invalid QR code format")
        return redirect('invalid')  # Redirect to an invalid page

    # Check if the code exists in the database
    if Ticket.objects.filter(code=code).exists():
        # If the ticket exists, fetch it
        ticket = Ticket.objects.get(code=code)
        
        # Check if the ticket has been used
        if ticket.is_used:
            print("Ticket already used")
            return redirect('scanned')  # Redirect to an invalid page
        else:
            # If the ticket is valid and not used
            ticket.is_used = True
            ticket.save()
            print("Ticket is valid")
            return redirect('valid')  # Redirect to a valid page
    else:
        # If the code does not exist or is not related to a valid ticket
        print("Ticket code does not exist in the database")
        return redirect('invalid')  # Redirect to an invalid page

    
def logout_view(request):
     logout(request)
     return redirect('login')

# Create your views here.
