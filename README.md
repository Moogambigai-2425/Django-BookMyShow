# Movie Booking System (Django)
## A cinema ticket reservation system with seat selection and recommendation features.

# Features
**Seat Availability Management:** Real-time seat status tracking per showtime

**Interactive Seat Selection:** Visual grid interface for seat reservations

**Movie Recommendations:** Suggests films based on user booking history

**Admin Dashboard:** Comprehensive backend for cinema management

# Technology Stack
**Framework:** Django 4.2

**Database:** PostgreSQL (Production), SQLite (Development)

**Authentication:** Django's built-in auth system

**Frontend:** JavaScript, CSS, HTML5

# Project Structure
movie-booking-system/
├── movies/                # Core booking functionality
│   ├── models.py          # Database models (Movies, Theaters, Seats)
│   ├── views.py           # Business logic for bookings
│   ├── admin.py           # Admin configurations
│   └── templates/         # HTML templates
│
├── users/                 # User management
│   ├── views.py           # Auth and profile management
│   └── models.py          # Custom user fields (if any)
│
├── static/                # CSS, JS, images
├── templates/             # Base templates
├── bookmyshow/            # Project configuration
└── requirements.txt       # Dependencies

# Installation

1. Clone repository:

git clone https://github.com/your-username/movie-booking-system.git

cd movie-booking-system

2. Create and activate virtual environment:

python -m venv venv

source venv/bin/activate  # Linux/macOS

venv\Scripts\activate     # Windows

3. Install dependencies:

pip install -r requirements.txt

4. Run database migrations:

python manage.py migrate

5. Create admin user:

python manage.py createsuperuser

Run development server:

6. Run development server:

python manage.py runserver

# Deployment Steps
## Frontend Deployment on Vercel:

Create a new project on Vercel.

Connect your GitHub repository or upload your project files.

Configure environment variables as needed, ensuring they match those required by your application.

Click on the "Deploy" button to initiate the deployment process.

## Backend Deployment on Render:

Sign up or log in to Render.

Create a new web service and select your backend repository.

Fill in the required environment variables, including your database connection string.

Start the deployment and monitor the logs for any issues.
