# QR Attendance System

A complete Django-based QR attendance system with student login and admin scanning capabilities.

## Features

✅ **Student Portal**
- Student registration and login
- Unique QR code generation containing: `student_id|name|class_name`
- View personal QR code on dashboard
- Track attendance records

✅ **Admin Portal**
- Admin login (staff users only)
- Real-time webcam QR code scanner using ZXing.js
- Instant attendance logging via AJAX
- Attendance reports with filters
- Download attendance as CSV

✅ **Technical Features**
- Django 4.2.8
- SQLite database
- Bootstrap 5 UI
- QR code generation with Pillow
- JavaScript QR scanner (ZXing library)
- CSRF protection
- Responsive design

## Project Structure

```
qr_attendance/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── media/
│   └── qr_codes/          # Generated QR code images
├── qr_attendance/
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # Project URLs
│   └── wsgi.py
├── attendance/
│   ├── __init__.py
│   ├── admin.py           # Admin configuration
│   ├── apps.py
│   ├── models.py          # Student & Attendance models
│   ├── views.py           # All views and API endpoints
│   ├── urls.py            # App URLs
│   ├── forms.py           # Login and registration forms
│   ├── static/
│   │   ├── js/
│   │   │   └── scanner.js
│   │   └── css/
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── student_login.html
│       ├── student_register.html
│       ├── student_dashboard.html
│       ├── admin_login.html
│       ├── admin_scanner.html
│       └── admin_report.html
```

## Installation & Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# or source venv/bin/activate # Linux/Mac
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

## Usage

### Student Flow
1. Go to home page → "I'm a Student"
2. Register new account or login
3. Dashboard shows your QR code
4. Share the QR code with admin for scanning

### Admin Flow
1. Go to home page → "I'm an Admin"
2. Login with staff credentials
3. Go to Scanner page
4. Allow camera access
5. Scan student QR codes
6. Attendance saved automatically
7. View reports and download CSV

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/save-attendance/` | Save attendance from scanned QR |
| GET | `/api/check-attendance/` | Check if student attended today |

## Models

### Student
- Linked to Django User
- Contains: phone, class_name, qr_code (image)
- Auto-generates QR code on creation

### Attendance
- Links student with date/time
- Status: present, absent, late
- Unique per student per day

## Key Features Explained

### QR Code Generation
- Uses Python `qrcode` library with Pillow
- Format: `student_id|name|class_name`
- Auto-generated on student creation
- Stored as PNG image in media folder

### Real-time Scanner
- Uses ZXing JavaScript library
- Accesses device camera via getUserMedia API
- Continuously scans for QR codes
- Sends detected data via AJAX to backend
- Instant feedback on successful/failed scans

### Attendance Logic
- One attendance record per student per day
- Automatically marked as "present" on scan
- Can be updated to "late" or "absent" by admin
- Unique constraint prevents duplicates

## Security Features
- CSRF tokens on all forms
- Password hashing with Django auth
- Staff-only admin access
- Input validation on QR parsing
- Error handling for invalid QR codes

## Database

SQLite database with the following tables:
- `auth_user` - Django user accounts
- `attendance_student` - Student profiles
- `attendance_attendance` - Attendance records

## Customization

### Change Secret Key (IMPORTANT)
In `qr_attendance/settings.py`:
```python
SECRET_KEY = 'your-new-secret-key-here'
```

### Use PostgreSQL Instead
Install: `pip install psycopg2-binary`
Update `settings.py` DATABASES section

### Add More Attendance Statuses
Edit `Attendance` model STATUS_CHOICES

### Customize QR Code Format
Modify `Student.generate_qr_code()` method

## Troubleshooting

### Camera not working
- Check browser permissions
- Use HTTPS in production
- Ensure camera is available and not in use

### QR code not generating
- Check media folder permissions
- Ensure Pillow is installed
- Check disk space

### Database errors
- Run migrations: `python manage.py migrate`
- Check database file permissions
- Delete db.sqlite3 and run migrations again

## Development

### Run with Hot Reload
```bash
python manage.py runserver --reload
```

### Create Superuser for Testing
```bash
python manage.py createsuperuser --username admin --email admin@example.com
```

### Access Django Admin
- URL: `http://localhost:8000/admin/`
- Manage students and attendance records

## Production Deployment

1. Set `DEBUG = False` in settings.py
2. Change SECRET_KEY
3. Use a production database (PostgreSQL)
4. Collect static files: `python manage.py collectstatic`
5. Use Gunicorn/uWSGI
6. Set up proper domain and SSL

## License
MIT License - Free to use and modify

## Support
For issues or questions, refer to Django documentation:
- https://docs.djangoproject.com/
- https://github.com/zxing-js/library
