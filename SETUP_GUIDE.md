# QR Attendance System - Getting Started Guide

## Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
python manage.py migrate
```

### Step 3: Create Admin User
```bash
python manage.py createsuperuser
# Enter username: admin
# Enter email: admin@example.com
# Enter password: (choose your password)
# Confirm password: (repeat password)
```

### Step 4: Run Server
```bash
python manage.py runserver
```

### Step 5: Access the System
- **Home Page**: http://localhost:8000/
- **Student Registration**: http://localhost:8000/student/register/
- **Student Login**: http://localhost:8000/student/login/
- **Admin Login**: http://localhost:8000/admin/login/
- **Django Admin**: http://localhost:8000/admin/

---

## Complete Workflow Example

### For Students:
1. Visit http://localhost:8000/student/register/
2. Fill in the registration form
3. You'll be able to login and see your QR code
4. Your QR code contains: `your_id|your_name|your_class`

### For Admin:
1. Login with superuser credentials at http://localhost:8000/admin/login/
2. Go to Scanner page
3. Allow camera access
4. Point camera at student QR code
5. Attendance is saved automatically

### To View Reports:
1. Login as admin
2. Go to Reports page
3. Filter by date or class
4. Download as CSV if needed

---

## File Descriptions

| File | Purpose |
|------|---------|
| `settings.py` | Django configuration, database, apps, templates |
| `urls.py` (project) | Main URL router to attendance app |
| `models.py` | Student and Attendance database models |
| `views.py` | All logic for login, scanning, reports |
| `forms.py` | User registration and login forms |
| `urls.py` (app) | Attendance app URL routes |
| `templates/` | HTML pages for UI |
| `admin.py` | Django admin customization |

---

## Database Models

### Student Model
```
- user (ForeignKey to Django User)
- phone (optional)
- class_name (required)
- qr_code (automatically generated image)
- created_at, updated_at
```

### Attendance Model
```
- student (ForeignKey)
- date (when attendance was recorded)
- time (exact time)
- status (present, absent, late)
- created_at
```

---

## API Endpoints

### 1. Save Attendance
```
POST /api/save-attendance/
Content-Type: application/json

Body: {
  "qr_data": "1|John Doe|10-A"
}

Response: {
  "success": true,
  "message": "Attendance marked for John Doe",
  "student_name": "John Doe",
  "student_class": "10-A"
}
```

### 2. Check Attendance
```
GET /api/check-attendance/?student_id=1

Response: {
  "exists": true/false
}
```

---

## Common Commands

```bash
# Run migrations
python manage.py migrate

# Create migrations from model changes
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access Django shell
python manage.py shell

# Create app backup
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json
```

---

## Customization Examples

### Change QR Code Data Format
Edit `attendance/models.py` in `Student.generate_qr_code()`:
```python
# Current: student_id|name|class_name
# Change to: student_id|email|phone
qr_data = f"{self.user.id}|{self.user.email}|{self.phone}"
```

### Add More Attendance Statuses
Edit `Attendance` model:
```python
STATUS_CHOICES = [
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
    ('sick_leave', 'Sick Leave'),  # Add new status
]
```

### Change Scanner Camera
In `admin_scanner.html`:
```javascript
// Currently: back camera
facingMode: 'environment'

// Change to: front camera
facingMode: 'user'
```

---

## Troubleshooting

### Issue: "Module not found: qrcode"
**Solution**: `pip install qrcode[pil]`

### Issue: "Media folder not found"
**Solution**: Create `media/qr_codes/` folder manually

### Issue: "PermissionError on QR code save"
**Solution**: Check folder permissions, run as administrator

### Issue: "Camera permission denied"
**Solution**: 
- Check browser settings
- Use HTTPS (required for production camera access)
- Try different browser

### Issue: "QR code not scanning"
**Solution**:
- Ensure good lighting
- QR code must be clear and not damaged
- Try moving closer to camera
- Check browser console for errors

---

## Next Steps

1. ✅ Install and run the project
2. ✅ Create some test students
3. ✅ Practice scanning QR codes
4. ✅ View attendance reports
5. ✅ Customize as needed for your use case

Good luck! 🎉
