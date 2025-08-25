# AI-Powered Customer Support System

A Django-based customer support system with AI integration using Google Gemini API for automated response generation.

## Features

- **User Authentication**: Separate roles for Customers and Admins (Support Agents)
- **Ticket Management**: Customers can submit tickets, admins can view and respond
- **AI Integration**: Google Gemini API for automated response suggestions
- **Admin Dashboard**: View all tickets and manage responses
- **Response Approval**: Admins can edit AI-generated responses before submitting

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Environment Variables
Copy the example environment file and add your Gemini API key:
```bash
cp .env.example .env
```
Edit `.env` and add your actual Gemini API key:
```
GEMINI_API_KEY=your-actual-gemini-api-key-here
```

### 3. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 5. Create Sample Categories (Optional)
Run the Django shell to create sample categories:
```bash
python manage.py shell
```
Then run:
```python
from support.models import Category
Category.objects.create(name="Technical", description="Technical support issues")
Category.objects.create(name="Billing", description="Billing and payment issues")
Category.objects.create(name="General", description="General inquiries")
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

## Usage

### For Customers:
1. Navigate to the home page
2. Submit support tickets with subject and message
3. View ticket status and responses

### For Admins:
1. Login with admin credentials
2. Access the admin dashboard to view all tickets
3. Click on a ticket to view details
4. Use "Generate AI Response" to get AI suggestions
5. Edit and submit responses

## API Integration

The system integrates with Google Gemini API for AI response generation. Make sure to:
1. Obtain a Gemini API key from Google AI Studio
2. Add the key to your `.env` file
3. The system will use the API to generate professional customer support responses

## Assumptions and Limitations

- Uses SQLite database (can be changed to PostgreSQL in settings)
- Basic authentication system (Django built-in)
- Simple frontend with Bootstrap
- AI responses are generated in real-time
- No email notifications implemented
- No file attachments for tickets

## Technologies Used

- **Backend**: Django 4.2.7
- **Database**: SQLite (default)
- **AI Integration**: Google Gemini API
- **Frontend**: Bootstrap 5
- **Authentication**: Django built-in auth

## File Structure

```
customer_support/
├── manage.py
├── requirements.txt
├── customer_support/          # Django project settings
├── support/                   # Main app
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── forms.py              # Form definitions
│   ├── gemini_integration.py # AI integration
│   └── templates/            # HTML templates
├── static/                   # Static files
└── .env                      # Environment variables
```

## Security Notes

- Change the default SECRET_KEY in production
- Use environment variables for sensitive data
- Consider using PostgreSQL in production
- Implement proper user role validation
- Add rate limiting for API calls

## Future Enhancements

- Email notifications
- File attachments
- Ticket prioritization
- Response templates
- Customer satisfaction ratings
- Advanced search and filtering
- Mobile-responsive design improvements
