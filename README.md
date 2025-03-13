# QR Check-In: Workplace Attendance Tracking System

## Overview
QR Check-In is a modern workplace attendance tracking system that combines QR code technology with geolocation verification to provide a reliable and efficient way to monitor employee attendance. The system allows employees to easily check in and out of workplaces using their smartphones, while providing administrators with accurate attendance records.

## Features
- **QR Code-Based Check-In/Out**: Employees can quickly check in and out by scanning workplace-specific QR codes
- **Geolocation Verification**: Ensures employees are physically present at the workplace location
- **Automatic Check-Out**: Automatically checks out employees at the end of shifts if they forget
- **User-Friendly Interface**: Simple and intuitive web interface for both employees and administrators
- **Detailed Attendance Reports**: Track attendance patterns and generate reports
- **Secure Authentication**: Role-based access control for different user types

## Installation

### Prerequisites
- Python 3.10+
- Django 4.2+
- Web server (e.g., Nginx, Apache)
- Database server (SQLite for development, MySQL recommended for production)

### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/qr_checkin_app.git
    cd qr_checkin_app
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Set up the automatic checkout cron job:
    ```bash
    python manage.py crontab add
    ```

## Usage

### Admin Setup
1. Log in to the admin panel at `http://localhost:8000/admin/`
2. Create workplaces with their locations
3. Add users and assign them to workplaces

### Employee Check-In/Out Process
1. Navigate to the login page and sign in
2. Scan the QR code at your workplace
3. Allow location access when prompted
4. The system will verify your location and record your check-in time
5. To check out, scan the QR code again

### Running the Automatic Checkout Job
The system includes a scheduled task that automatically checks out employees who forget to do so:
- Employees who checked in before 5 PM are checked out at 5 PM
- Employees who checked in after 5 PM (overtime) are checked out at 11:59:59 PM

## Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=America/New_York
```

### Settings Configuration
Key settings can be modified in `checkin_app/settings.py`:
- `TIME_ZONE`: Set your local timezone
- `CRONJOBS`: Configure the automatic checkout schedule
- `STATICFILES_DIRS`: Configure static file locations

## API Access
The system provides API endpoints for integration with other systems:
- `/api/attendance/`: Get attendance records
- `/api/workplaces/`: Get workplace information

API authentication requires an API key that can be generated in the admin interface.

## Development

### Project Structure
```
QR_checkin_app/
├── checkin/                # Main application
│   ├── management/         # Management commands
│   ├── migrations/         # Database migrations
│   ├── static/             # Static assets
│   ├── templates/          # HTML templates
│   ├── models.py           # Data models
│   ├── views.py            # View controllers
│   ├── urls.py             # URL routing
│   └── tasks.py            # Background tasks
├── checkin_app/            # Project settings
├── media/                  # User-uploaded files
├── manage.py               # Django management script
└── requirements.txt        # Project dependencies
```

### Running Tests
```bash
python manage.py test
```

## Deployment
For production deployment:
1. Set `DEBUG=False` in settings
2. Configure a production database
3. Set up a web server (Nginx/Apache)
4. Configure HTTPS
5. Set up the crontab for automatic checkout

## License
[MIT License](LICENSE)

## Support
For support, contact [kaanbalta57@gmail.com](mailto:kaanbalta57@gmail.com)


## Acknowledgements
- Django framework
- [QR Code Generator Library](https://pypi.org/project/qrcode/)
- [GeoPy](https://pypi.org/project/geopy/) for geolocation calculations

---
*This project was developed by Korkut Kaan Balta © 2025*
