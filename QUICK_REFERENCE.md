# QR Attendance System - Quick Reference Card

## 📌 Command Cheat Sheet

### Initial Setup
```bash
# 1. Navigate to project
cd "c:\Users\amarr\Desktop\Python class\qr_attendance"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Start server
python manage.py runserver
```

### Regular Operations
```bash
# Run server
python manage.py runserver

# Run tests
python manage.py test attendance

# Access Python shell
python manage.py shell

# Backup database
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json

# Create demo data
python manage.py shell < create_demo_data.py

# Collect static files (production)
python manage.py collectstatic

# Make database changes
python manage.py makemigrations
python manage.py migrate
```

---

## 🔑 Default Test Credentials

Once you run the setup, use these credentials:

**Student Account:**
```
Email: student1@example.com
Password: student123
```

**Admin Account:**
```
Username: admin
Password: [as you created]
```

**Django Admin:**
```
URL: http://localhost:8000/admin/
Username: [your superuser]
Password: [your password]
```

---

## 🌐 Important URLs

| Page | URL | Purpose |
|------|-----|---------|
| Home | `http://localhost:8000/` | Navigation hub |
| Student Register | `/student/register/` | Create account |
| Student Login | `/student/login/` | Login to portal |
| Student Dashboard | `/student/dashboard/` | View QR code |
| Admin Login | `/admin/login/` | Admin access |
| QR Scanner | `/admin/scanner/` | Scan QR codes |
| Reports | `/admin/report/` | View attendance |
| Django Admin | `/admin/` | Database management |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `settings.py` | Database, apps, templates config |
| `models.py` | Student & Attendance models |
| `views.py` | All logic & APIs |
| `forms.py` | Login/registration forms |
| `urls.py` | URL routing |
| `admin_scanner.html` | QR scanner page |
| `student_dashboard.html` | QR code display |

---

## 🔧 Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| "Module not found: qrcode" | `pip install qrcode[pil]` |
| "Media folder not found" | Create `media/qr_codes/` manually |
| "Camera not working" | Check browser permissions |
| "Database locked" | Delete `db.sqlite3` and run migrate |
| "Static files missing" | Run `python manage.py collectstatic` |

---

## 📊 Database Operations

```bash
# Enter Django shell
python manage.py shell

# Create a student manually
from django.contrib.auth.models import User
from attendance.models import Student

user = User.objects.create_user(
    username='john',
    email='john@example.com',
    password='pass123',
    first_name='John',
    last_name='Doe'
)

student = Student.objects.create(
    user=user,
    phone='9876543210',
    class_name='10-A'
)

# View all students
from attendance.models import Student
students = Student.objects.all()
for s in students:
    print(f"{s.user.get_full_name()} - {s.class_name}")

# View today's attendance
from attendance.models import Attendance
from datetime import date
today = Attendance.objects.filter(date=date.today())
for att in today:
    print(f"{att.student} - {att.status}")

# Delete a student
user = User.objects.get(username='john')
user.delete()  # This also deletes related Student
```

---

## 🎨 Customization Snippets

### Add New Attendance Status
File: `attendance/models.py`
```python
STATUS_CHOICES = [
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
    ('excused', 'Excused Leave'),  # NEW
]
```

### Change QR Code Format
File: `attendance/models.py` → `generate_qr_code()` method
```python
# Change from:
qr_data = f"{self.user.id}|{self.user.get_full_name()}|{self.class_name}"

# To:
qr_data = f"{self.user.id}|{self.user.email}|{self.phone}"
```

### Customize Scanner Camera
File: `attendance/templates/admin_scanner.html`
```javascript
// Line with: facingMode: 'environment'
// Change to:
facingMode: 'user'  // For selfie camera
```

### Add Bootstrap Theme
File: `attendance/templates/base.html`
```html
<!-- Replace the Bootstrap CDN link with: -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
```

---

## 🧪 Testing Guide

### Run Unit Tests
```bash
python manage.py test attendance
```

### Create Test Data
```python
from django.contrib.auth.models import User
from attendance.models import Student, Attendance
from datetime import datetime, date

# Create test student
user = User.objects.create_user(
    username='testuser',
    email='test@test.com',
    password='test123'
)

student = Student.objects.create(
    user=user,
    class_name='10-A'
)

# Create test attendance
attendance = Attendance.objects.create(
    student=student,
    date=date.today(),
    time=datetime.now().time(),
    status='present'
)
```

### Test API Endpoints
```bash
# Using curl (Windows: install curl or use Postman)
curl -X POST http://localhost:8000/api/save-attendance/ \
  -H "Content-Type: application/json" \
  -d '{"qr_data":"1|John Doe|10-A"}'
```

---

## 🚀 Performance Tips

1. **Use Admin Panel** for bulk operations
2. **Create indexes** for frequently filtered fields
3. **Use pagination** for large attendance lists
4. **Cache QR codes** to prevent regeneration
5. **Archive old records** periodically
6. **Use PostgreSQL** for production (not SQLite)

---

## 🔐 Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG = False in production
- [ ] Use HTTPS in production
- [ ] Set secure cookies
- [ ] Add ALLOWED_HOSTS
- [ ] Use environment variables for secrets
- [ ] Regularly update dependencies
- [ ] Validate all user inputs
- [ ] Use CSRF tokens (already enabled)
- [ ] Hash passwords (Django does this)

---

## 📱 Browser Compatibility

✅ Chrome/Chromium (Best)
✅ Firefox
✅ Safari
✅ Edge
✅ Mobile browsers

❌ Internet Explorer (Not supported)

---

## 🐳 Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "qr_attendance.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build & Run:
```bash
docker build -t qr-attendance .
docker run -p 8000:8000 qr-attendance
```

---

## 📈 Project Statistics

| Metric | Count |
|--------|-------|
| Python Files | 10 |
| HTML Templates | 8 |
| Models | 2 |
| Views | 12 |
| URLs | 13 |
| Form Classes | 3 |
| Lines of Code | ~2,500 |
| Documentation Pages | 4 |

---

## 🎓 Learning Resources

- **Django Official**: https://docs.djangoproject.com/
- **ZXing.js Scanner**: https://github.com/zxing-js/library
- **Bootstrap Framework**: https://getbootstrap.com/
- **Python Docs**: https://docs.python.org/3/
- **HTML/CSS/JS**: https://developer.mozilla.org/

---

## 💬 Common Q&A

**Q: How to add more admin users?**
```bash
python manage.py createsuperuser
# or use Django admin at /admin/
```

**Q: Can I run on port 8080?**
```bash
python manage.py runserver 8080
```

**Q: How to reset the database?**
```bash
rm db.sqlite3
python manage.py migrate
```

**Q: How to export all data?**
```bash
python manage.py dumpdata > data.json
```

**Q: How to backup QR code images?**
```bash
# Copy the entire media/ folder
# All QR codes are stored in: media/qr_codes/
```

---

## 🆘 Getting Help

1. **Check Django Logs**: Look at console output for errors
2. **Django Shell**: Use `python manage.py shell` to debug
3. **Django Admin**: View/edit data at `/admin/`
4. **Browser Console**: F12 to check JavaScript errors
5. **Check Documentation**: Read PROJECT_SUMMARY.md, README.md, SETUP_GUIDE.md

---

## 📅 Common Development Workflow

```
┌─ Start Day
│
├─ Activate virtual environment
│  └─ venv\Scripts\activate (Windows)
│
├─ Run Django server
│  └─ python manage.py runserver
│
├─ Make code changes
│
├─ Test changes
│  ├─ Browser: http://localhost:8000/
│  └─ Tests: python manage.py test
│
├─ Commit changes
│  └─ git commit -am "message"
│
└─ End Day
   └─ Stop server (Ctrl+C)
```

---

## 🎉 Success Indicators

✅ If you see these, everything works:
- Home page loads at `/`
- Student registration succeeds
- Student QR code displays
- Admin can scan QR codes
- Attendance saved successfully
- CSV download works
- Django admin loads at `/admin/`

---

**Version**: 1.0.0  
**Last Updated**: November 15, 2025  
**Status**: ✅ Production Ready
