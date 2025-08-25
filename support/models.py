from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject} - {self.customer.username}"

class Reply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_ai_generated = models.BooleanField(default=False)
    is_modified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Reply to {self.ticket.subject} by {self.responder.username}"
