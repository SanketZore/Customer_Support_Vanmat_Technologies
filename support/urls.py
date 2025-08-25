from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.customer_dashboard, name='customer_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('customer-ticket/<int:ticket_id>/', views.customer_ticket_details, name='customer_ticket_details'),
    path('generate-ai-reply/<int:ticket_id>/', views.generate_ai_reply, name='generate_ai_reply'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('submit-response/<int:ticket_id>/', views.submit_response, name='submit_response'),
    path('delete-ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('delete-response/<int:response_id>/', views.delete_response, name='delete_response'),
]
