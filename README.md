# PhysioGhar — Therapist App Backend

This is the Django REST API backend for the **PhysioGhar Therapist App** technical assignment.

The backend handles authentication, therapist profile, availability, schedules, booking requests, sessions, patients, patient notes, and complaints. The Flutter application communicates with this backend using REST APIs.

---

## Tech Stack

* Python 3.14.7
* Django 6.1.1
* Django REST Framework 3.18.1
* SimpleJWT 5.5.1
* PostgreSQL
* django-filter
* django-cors-headers
* Pillow
* python-dotenv

---

## Main Features

* JWT authentication
* Therapist profile and profile updates
* Therapist availability
* Schedule and time-slot management
* Booking requests
* Accept / decline booking requests
* Session rescheduling
* Session completion and cancellation
* Patient records
* Patient treatment history
* Patient notes
* Complaints / Report an Issue
* Django Admin

---

## Project Structure

```text
physioghar-backend/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
├── patients/
├── schedules/
├── session_management/
├── complaints/
│
├── media/
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

The project is divided into separate Django apps so that authentication, patients, schedules, sessions, and complaints can be maintained independently.

---

# Setup

## 1. Clone the Repository

```bash
git clone <BACKEND_REPOSITORY_URL>
cd physioghar-backend
```

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Setup

This project uses **PostgreSQL** as the database.

Make sure PostgreSQL is installed and running on your machine.

Create a database, for example:

```sql
CREATE DATABASE physioghar_db;
```

You can use any database name, but make sure it matches the value in your `.env` file.

---

# Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True

SECRET_KEY=your-secret-key

DB_NAME=physioghar_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5432
```

Update the database username and password according to your local PostgreSQL setup.

> Do not commit the `.env` file or database credentials to GitHub.

---

# Database Migration

After configuring the database, run:

```bash
python manage.py migrate
```

This will create all required database tables.

---

# Create a Superuser

To access the Django Admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create the username, email, and password.

---

# Run the Backend

For normal local development:

```bash
python manage.py runserver
```

The server will be available at:

```text
http://127.0.0.1:8000/
```

For testing the Flutter application on a physical Android device, run:

```bash
python manage.py runserver 0.0.0.0:8000
```

Then use your computer's local network IP as the API base URL in the Flutter application:

```text
http://YOUR_LOCAL_IP:8000/api/v1
```

For example:

```text
http://192.168.1.100:8000/api/v1
```

The computer and Android device should be connected to the same Wi-Fi network.

---

# Django Admin

After creating a superuser, open:

```text
http://127.0.0.1:8000/admin/
```

and log in using the superuser credentials.

When testing from another device on the same network, the admin can also be accessed using:

```text
http://YOUR_LOCAL_IP:8000/admin/
```

---

# API

The main API is available under:

```text
/api/v1/
```

The API uses JWT authentication.

Example:

```text
Authorization: Bearer <access_token>
```

The backend currently provides APIs for:

* Authentication
* Therapist profiles
* Availability
* Schedule slots
* Booking requests
* Sessions
* Patients
* Patient notes
* Complaints

---

# Flutter App Connection

The Flutter app uses **Dio** to communicate with this backend.

For a physical Android device, update the Flutter API base URL to the computer's local IP:

```text
http://YOUR_LOCAL_IP:8000/api/v1
```

For example:

```text
http://192.168.1.100:8000/api/v1
```

Make sure:

1. The backend is running with `0.0.0.0:8000`.
2. The computer and phone are on the same Wi-Fi network.
3. The correct local IP is used in the Flutter application.

---

# Authentication

Authentication is implemented using **Django REST Framework + SimpleJWT**.

The backend uses:

* Access tokens
* Refresh tokens
* Bearer authentication
* Token blacklist support

The Flutter application stores authentication tokens securely and uses the access token when making authenticated API requests.

---

# Main Application Flow

The backend supports the main flows required by the assignment.

### Booking / Session Flow

```text
Booking Request
      ↓
Accept
      ↓
Upcoming Session
      ↓
Complete
      ↓
Completed Session
```

A booking request can also be declined:

```text
Booking Request
      ↓
Decline
      ↓
Cancelled
```

### Schedule Flow

Schedule slots can change between different states:

```text
OPEN → BLOCKED
BLOCKED → OPEN
```

When a booking is accepted:

```text
OPEN → BOOKED
```

The backend validates these state changes so that the Flutter application can reflect the current schedule and session status.

---

# Development / Testing Note

For local development and physical Android device testing, the backend
allows requests from the local development hosts configured in
`ALLOWED_HOSTS`.

The current development configuration includes:

```python
ALLOWED_HOSTS = [
    "192.168.1.69",
    "localhost",
    "127.0.0.1",
]

# Email Configuration

For the current assignment setup, email uses Django's console email backend.

This means email-related messages are displayed in the development server console instead of being sent through a real email provider.

A production version can be configured with an actual SMTP or email service.

---

# Media Files

User-uploaded media such as profile images are stored under:

```text
media/
```

The project uses Django's `MEDIA_URL` and `MEDIA_ROOT` configuration for handling uploaded files.

---

# Running the Project from Scratch

The basic setup is:

```bash
python -m venv venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Create and configure the PostgreSQL database and `.env` file.

Then run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

For physical Android testing:

```bash
python manage.py runserver 0.0.0.0:8000
```

---

# Future Improvements

If this project were continued beyond the assignment, I would consider adding:

* Production deployment configuration
* API documentation using Swagger / OpenAPI
* More automated tests
* Production email and notification services
* Better environment-specific settings
* Real-time notifications
* More detailed logging and monitoring
* Additional security and production hardening
* CI/CD improvements

---

## Assignment

This backend was developed as part of the **PhysioGhar Flutter Developer Technical Assignment**.

The Flutter frontend and this Django backend are connected and were tested together on a physical Android device.

**Frontend:** Flutter + Riverpod
**Backend:** Django REST Framework + PostgreSQL
