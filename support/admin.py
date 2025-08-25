from django.contrib import admin
from .models import Category, Ticket, Reply

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'customer', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['subject', 'message', 'customer__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'responder', 'is_ai_generated', 'created_at']
    list_filter = ['is_ai_generated', 'created_at']
    search_fields = ['message', 'ticket__subject', 'responder__username']
    readonly_fields = ['created_at']
