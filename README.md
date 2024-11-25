# EcoGather

**EcoGather** is an innovative platform that allows event organizers to streamline their operations by creating, sharing, and reusing digital bulletins for events. It supports features like customizable templates, event tracking, and public or private event settings, all while promoting sustainability by reducing paper waste.

---

## Features
- **Event Management**: Organizers can create and manage events with public or private visibility.
- **Custom Bulletin Templates**: Design reusable templates with customizable fields.
- **Template Cloning**: Easily clone and edit templates for recurring or similar events.
- **User Access Control**:
  - Anonymous users can access public templates.
  - Authenticated users can access their own templates and public templates.
  - Staff users have full access.
- **Download Tracking**: Track template downloads for attendance insights.
- **Sustainability Impact**: Contribute to reducing paper waste by promoting digital solutions.

---

## Setup Guide

### Prerequisites
1. Python 3.10 or higher.
2. PostgreSQL database.
3. Virtual environment tools (e.g., `venv` or `pipenv`).

---

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/EcoGather.git
   cd EcoGather


Install Dependencies

bash
Copy code
pip install -r requirements.txt
Set Up the Environment Variables Create a .env file in the project root and configure the following:

makefile
Copy code
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://username:password@localhost:5432/ecogather_db
Apply Migrations

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a Superuser

bash
Copy code
python manage.py createsuperuser
Run the Development Server

bash
Copy code
python manage.py runserver
Access the application at http://127.0.0.1:8000.

API Endpoints
Authentication
POST /auth/login/: Log in a user.
POST /auth/register/: Register a new user.
Events
GET /api/events/: List all events (public and private based on permissions).
POST /api/events/: Create a new event (authenticated users only).
GET /api/events/<id>/: Retrieve a single event.
Templates
GET /api/templates/: List templates (permissions apply).
POST /api/templates/: Create a new template (authenticated users only).
PATCH /api/templates/<id>/: Update a template (owner only).
POST /api/templates/<id>/clone/: Clone a template.
Custom Fields
POST /api/templates/<id>/fields/: Add a custom field to a template (owner only).
PATCH /api/templates/fields/<id>/: Update a custom field.
Testing
Run the test suite to ensure everything works as expected:

bash
Copy code
python manage.py test

