from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from .models import Ticket, Category, Reply
from .forms import TicketForm

@login_required
def customer_dashboard(request):
    # Redirect admins to admin dashboard
    if request.user.is_staff:
        return redirect('admin_dashboard')
    
    tickets = Ticket.objects.filter(customer=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.save()
            messages.success(request, 'Ticket submitted successfully!')
            return redirect('customer_dashboard')
    else:
        form = TicketForm()
    
    return render(request, 'support/customer_dashboard.html', {
        'tickets': tickets,
        'form': form
    })

@login_required
def submit_response(request, ticket_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('customer_dashboard')
    
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Use the form to handle the response
    from .forms import ReplyForm
    form = ReplyForm(request.POST)
    
    if form.is_valid():
        response = form.cleaned_data['message'].strip()
        
        # Validate response - must not be empty or only whitespace
        if not response:
            messages.error(request, 'Response cannot be empty. Please provide a proper message.')
            return redirect('admin_dashboard')
        
        # Create a reply for the ticket
        ticket.status = 'replied'
        ticket.save()
        
        # Save the response
        Reply.objects.create(
            ticket=ticket, 
            responder=request.user, 
            message=response,
            is_ai_generated=form.cleaned_data.get('is_ai_generated', False)
        )
        
        messages.success(request, 'Response submitted successfully!')
        return redirect('admin_dashboard')
    else:
        # If form is invalid, show errors
        messages.error(request, 'Please provide a valid response.')
        return redirect('admin_dashboard')

@login_required
def admin_dashboard(request):
    # Only allow staff users to access admin dashboard
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('customer_dashboard')
    
    tickets = Ticket.objects.all().order_by('-created_at')
    if request.method == 'POST':
        # Use the form to handle the response
        from .forms import ReplyForm
        form = ReplyForm(request.POST)
        
        if form.is_valid():
            response = form.cleaned_data['message'].strip()
            ticket_id = request.POST.get('ticket_id')
            ticket = get_object_or_404(Ticket, id=ticket_id)
            
            # Validate response - must not be empty or only whitespace
            if not response:
                messages.error(request, 'Response cannot be empty. Please provide a proper message.')
                return redirect('admin_dashboard')
            
            # Create a reply for the ticket
            ticket.status = 'replied'
            ticket.save()
            
            # Save the response
            Reply.objects.create(
                ticket=ticket, 
                responder=request.user, 
                message=response,
                is_ai_generated=form.cleaned_data.get('is_ai_generated', False)
            )
            
            messages.success(request, 'Response submitted successfully!')
            return redirect('admin_dashboard')
        else:
            # If form is invalid, show errors
            messages.error(request, 'Please provide a valid response.')
            return redirect('admin_dashboard')
    
    # Create form for response
    from .forms import ReplyForm
    form = ReplyForm()
    
    return render(request, 'support/admin_dashboard.html', {
        'tickets': tickets,
        'form': form
    })

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check if user has permission to view this ticket
    if not request.user.is_staff and ticket.customer != request.user:
        messages.error(request, 'Access denied.')
        return redirect('customer_dashboard')
    
    replies = ticket.replies.all()
    
    # Handle form submission
    if request.method == 'POST':
        from .forms import ReplyForm
        form = ReplyForm(request.POST)
        
        if form.is_valid():
            response = form.cleaned_data['message'].strip()
            
            # Validate response - must not be empty or only whitespace
            if not response:
                messages.error(request, 'Response cannot be empty. Please provide a proper message.')
                return redirect('ticket_detail', ticket_id=ticket_id)
            
            # Create a reply for the ticket
            ticket.status = 'replied'
            ticket.save()
            
            # Save the response
            Reply.objects.create(
                ticket=ticket, 
                responder=request.user, 
                message=response,
                is_ai_generated=form.cleaned_data.get('is_ai_generated', False)
            )
            
            messages.success(request, 'Response submitted successfully!')
            return redirect('ticket_detail', ticket_id=ticket_id)
        else:
            # If form is invalid, show errors
            messages.error(request, 'Please provide a valid response.')
            return redirect('ticket_detail', ticket_id=ticket_id)
    else:
        # Create form for response
        from .forms import ReplyForm
        form = ReplyForm()
    
    return render(request, 'support/ticket_detail.html', {
        'ticket': ticket, 
        'replies': replies,
        'form': form
    })

@login_required
def customer_ticket_details(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check if user has permission to view this ticket
    if ticket.customer != request.user:
        messages.error(request, 'Access denied.')
        return redirect('customer_dashboard')
    
    replies = ticket.replies.all()
    return render(request, 'support/customer_ticket_details.html', {'ticket': ticket, 'replies': replies})

def generate_ai_reply(request, ticket_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    try:
        # Use Grok API integration instead of Gemini
        from .grok_integration import generate_grok_response
        ai_reply = generate_grok_response(ticket.subject, ticket.message)
        return JsonResponse({'success': True, 'reply': ai_reply})
    except Exception as e:
        # Return a proper error message
        return JsonResponse({'success': False, 'error': str(e)})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')
    
    return render(request, 'support/register.html')

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check if user has permission to delete this ticket
    # Allow deletion if user is admin OR if user is the ticket owner
    if not request.user.is_staff and ticket.customer != request.user:
        messages.error(request, 'Access denied. You can only delete your own tickets.')
        return redirect('customer_dashboard')
    
    ticket.delete()
    messages.success(request, 'Ticket deleted successfully!')
    
    # Redirect to appropriate dashboard based on user role
    if request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('customer_dashboard')

@login_required
def delete_response(request, response_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('customer_dashboard')
    
    response = get_object_or_404(Reply, id=response_id)
    ticket_id = response.ticket.id
    response.delete()
    messages.success(request, 'Response deleted successfully!')
    return redirect('ticket_detail', ticket_id=ticket_id)

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('customer_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'support/login.html')
