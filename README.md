# EcoGather: Event Management Platform

EcoGather is an innovative platform designed to streamline event creation, management, and participation. By integrating powerful features like QR code generation and reusable templates, EcoGather empowers organizers to manage events effectively while enhancing attendee experiences.

## MVP (Minimum Viable Product) Features

### 1.**User Registration, Login, and Logout**

   -Authentication system using JWT tailored for event organizers.
   -Provides secure access to event management tools.

### 2.**Event Creation and Management**

   - Organizers can create, edit, and manage event details, including:
     -Event title, description, and location.
     -Start and end times.
     -Public or private visibility settings.

### 3.**Templates and Custom Fields**

   -Add custom fields to capture specific event details.

### 4. **QR Code Generation**

   -Generate unique QR codes for each event.
   -Use QR codes to share event details

### 5. **Event Listings**

   -Display upcoming events with filters by category, date, or organizer.
   -Attendees can browse public events without logging in.

### 6.**Image Uploads**

   -Organizers can upload event images and theirs.
   -Set priority images to highlight specific details.

### 7.**Contact Information**
   -Organizers can provide their contact details for attendee inquiries.

## Additional Planned Features

- **Event Status**: Dynamically determine and display event status (upcoming, ongoing, ended).
- **Organizer Profiles**: Showcase past and upcoming events by an organizer.


## Setup Guide

### Prerequisites
1. **Python** (v3.8 or higher)
2. **Django** (v4.0 or higher)
3. **PostgreSQL** (or any other supported database)
4. **Virtual Environment Tool** (e.g., `venv` or `virtualenv`)
---

### Installation

1.**Clone the Repository**

   git clone https://github.com/your-repo/EcoGather.git
   cd EcoGather

2.**Install Dependencies**

> pip install -r requirements.txt
Set Up the Environment Variables Create a .env file in the project root and configure the following:

4.**Makemigration and migrate**

python manage.py makemigrations
python manage.py migrate
Create a Superuser

5.**Create super user**

python manage.py createsuperuser
> password won't show, make sure you input the right one.

6.**Run the Development Server**

python manage.py runserver
Access the application at http://127.0.0.1:8000.

