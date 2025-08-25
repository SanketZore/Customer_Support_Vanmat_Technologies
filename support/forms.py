from django import forms
from .models import Ticket, Reply, Category

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'message', 'category']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your issue',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'subject': 'Subject',
            'message': 'Message',
            'category': 'Category (optional)',
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['message', 'is_ai_generated']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your response',
                'rows': 4,
                'id': 'reply-message'
            }),
            'is_ai_generated': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'message': 'Response',
            'is_ai_generated': 'AI Generated',
        }
