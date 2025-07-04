# Django HTMX Project

A modern Django web application demonstrating HTMX (Hypertext Markup Language Extensions) integration for dynamic, interactive web interfaces without heavy JavaScript frameworks.

## 🚀 Features

- **HTMX Integration**: Dynamic content loading and form submissions without page refreshes
- **Bootstrap 5 UI**: Modern, responsive design with Bootstrap 5 and Bootstrap Icons
- **DataTables**: Interactive data tables with sorting, filtering, and pagination
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality for all models
- **Form Management**: Dynamic form handling with Django Crispy Forms
- **API Endpoints**: RESTful API endpoints for data operations
- **Modular Architecture**: Well-organized code structure with separate views, forms, and utilities

## 📋 Models

The application includes the following data models:

- **Person**: Authors and editors with role-based management
- **Publisher**: Book publishing companies
- **Book**: Books with details like pages, price, rating, and publication date
- **Store**: Book stores
- **StoreBook**: Junction table linking stores and books with inventory information

## 🛠️ Technology Stack

- **Backend**: Django 5.2.1
- **Frontend**: HTMX, Bootstrap 5, jQuery
- **Database**: SQLite (default)
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Tables**: DataTables for enhanced data display
- **Icons**: Bootstrap Icons

## 📦 Dependencies

- Django 5.2.1
- django-htmx 1.23.0
- django-crispy-forms 2.4
- crispy-bootstrap5 2025.4
- asgiref 3.8.1
- sqlparse 0.5.3

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd django_htmx_project
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
django_htmx_project/
├── django_htmx_project/          # Main project settings
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py                   # WSGI configuration
├── myapp/                        # Main application
│   ├── models.py                 # Database models
│   ├── views/                    # View modules
│   │   ├── web/                  # Web views
│   │   └── api/                  # API views
│   ├── forms/                    # Form modules
│   ├── utils/                    # Utility functions
│   └── urls.py                   # App URL configuration
├── templates/                    # HTML templates
│   ├── base.html                 # Base template
│   ├── navbar.html               # Navigation component
│   └── myapp/                    # App-specific templates
├── static/                       # Static files
├── media/                        # User-uploaded files
├── requirements.txt              # Python dependencies
└── manage.py                     # Django management script
```

## 🎯 Key Features Explained

### HTMX Integration

The project uses HTMX for dynamic interactions:

- **Dynamic Form Loading**: Forms are loaded via HTMX requests without page refreshes
- **Real-time Updates**: Content updates happen seamlessly in the background
- **Progressive Enhancement**: Works without JavaScript, enhanced with HTMX

### Bootstrap 5 UI

- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Modern Components**: Cards, modals, alerts, and form styling
- **Icon Integration**: Bootstrap Icons for enhanced visual appeal

### DataTables Integration

- **Interactive Tables**: Sortable, searchable, and paginated data tables
- **Column Controls**: Show/hide columns dynamically
- **Export Options**: Data export functionality
- **Responsive Tables**: Mobile-friendly table display

## 🔧 Configuration

### Environment Variables

The project uses Django's default settings. For production, consider:

- Setting `DEBUG = False`
- Configuring a production database
- Setting up proper `SECRET_KEY`
- Configuring `ALLOWED_HOSTS`

### Static Files

Static files are served from the `static/` directory and configured in `settings.py`:

```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

## 🚀 Usage

### Dashboard

Visit the main dashboard at `http://127.0.0.1:8000/` to see an overview of the application.

### CRUD Operations

The application provides full CRUD functionality for all models:

- **Person Management**: `/person/` - Manage authors and editors
- **Publisher Management**: `/publisher/` - Manage publishing companies
- **Book Management**: `/book/` - Manage books and their details
- **Store Management**: `/store/` - Manage book stores and inventory

### API Endpoints

RESTful API endpoints are available for programmatic access:

- `/api/person/` - Person API
- `/api/publisher/` - Publisher API
- `/api/book/` - Book API
- `/api/store/` - Store API

### HTMX Features

- **Dynamic Forms**: Add/remove form fields dynamically
- **Inline Editing**: Edit content without page navigation
- **Real-time Search**: Search functionality with instant results
- **Progressive Loading**: Load content as needed

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Support

For support and questions, please open an issue in the repository or contact the development team.

---

**Happy Coding! 🎉**
