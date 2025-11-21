# QR Attendance System - Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    QR ATTENDANCE SYSTEM                      │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼────────┐     ┌───────▼────────┐
        │  STUDENT SIDE  │     │   ADMIN SIDE   │
        └────────────────┘     └────────────────┘
                │                       │
        ┌───────▼──────────────┐        │
        │  Student Portal      │        │
        ├──────────────────────┤        │
        │ • Register/Login     │        │
        │ • View QR Code       │        │
        │ • View Attendance    │        │
        └──────────┬───────────┘        │
                   │                    │
                   │              ┌─────▼──────────────┐
                   │              │  Admin Portal      │
                   │              ├────────────────────┤
                   │              │ • Login            │
                   │              │ • Scan QR Code     │
                   │              │ • View Reports     │
                   │              │ • Download CSV     │
                   │              └─────┬──────────────┘
                   │                    │
                   │    ┌───────────────┴──────────────┐
                   │    │                              │
                   └────▼──────────────────────────────┘
                        │
            ┌───────────▼───────────┐
            │   DJANGO BACKEND      │
            ├───────────────────────┤
            │  • Models (Student,   │
            │    Attendance)        │
            │  • Views & APIs       │
            │  • Forms & Auth       │
            │  • QR Generation      │
            └───────────┬───────────┘
                        │
            ┌───────────▼───────────┐
            │   SQLite Database     │
            ├───────────────────────┤
            │  • Users              │
            │  • Students           │
            │  • Attendance Records │
            │  • QR Code Images     │
            └───────────────────────┘
```

---

## Student Registration & Login Flow

```
START
  │
  ├─▶ Visit /student/register/
  │     │
  │     └─▶ Fill Registration Form
  │           │
  │           ├─ Username
  │           ├─ Email
  │           ├─ Password
  │           ├─ Name
  │           ├─ Phone
  │           └─ Class
  │           │
  │           ▼
  │     Validate Input
  │           │
  │     ✓─▶ Create User
  │           │
  │           ▼
  │     Create Student Profile
  │           │
  │           ▼
  │     AUTO: Generate QR Code
  │           │
  │           ▼
  │     Redirect to Login
  │
  ├─▶ Visit /student/login/
  │     │
  │     ├─ Enter Email
  │     ├─ Enter Password
  │           │
  │           ▼
  │     Authenticate User
  │           │
  │     ✓─▶ Create Session
  │           │
  │           ▼
  │     Redirect to Dashboard
  │
  ├─▶ /student/dashboard/
  │     │
  │     ├─ Display Profile Info
  │     ├─ Display QR Code Image
  │     └─ Display Attendance History
  │
  └─▶ LOGGED IN ✓
```

---

## Admin Scanner & Attendance Flow

```
ADMIN WORKFLOW
  │
  ├─▶ Visit /admin/login/
  │     │
  │     ├─ Enter Username
  │     ├─ Enter Password
  │           │
  │           ▼
  │     Check is_staff = True
  │           │
  │     ✓─▶ Authenticate & Login
  │           │
  │           ▼
  │     Redirect to Scanner
  │
  ├─▶ /admin/scanner/
  │     │
  │     ├─ Request Camera Permission
  │     │     │
  │     │     ▼
  │     │  User Allows Access ✓
  │     │     │
  │     │     ▼
  │     │  Initialize Video Stream
  │     │     │
  │     │     ▼
  │     │  Load ZXing.js Library
  │     │     │
  │     │     ▼
  │     │  Start QR Detection Loop
  │     │     │
  │     │     ▼
  │     │  SCANNING... (waiting for QR)
  │     │     │
  │     │     ├─▶ QR Code Detected!
  │     │           │
  │     │           ▼
  │     │     Extract QR Data
  │     │     Format: student_id|name|class
  │     │           │
  │     │           ▼
  │     │     Send AJAX POST to /api/save-attendance/
  │     │           │
  │     │           ▼
  │     │     BACKEND PROCESSING:
  │     │     ├─ Parse QR Data
  │     │     ├─ Find Student
  │     │     ├─ Validate Data
  │     │     ├─ Check Unique Today
  │     │     └─ Save Attendance Record
  │     │           │
  │     │           ▼
  │     │     Return JSON Response
  │     │     {success, student_name, class}
  │     │           │
  │     │           ▼
  │     │     Display Success Message ✓
  │     │     │
  │     │     └─▶ Continue Scanning...
  │     │
  │     └─▶ LOOP: Repeat for next student
  │
  └─▶ END
```

---

## Database Schema

```
┌──────────────────────────────────────────┐
│          Django User Table               │
├──────────────────────────────────────────┤
│ id (PK)                                  │
│ username (UNIQUE)                        │
│ email (UNIQUE)                           │
│ password (hashed)                        │
│ first_name                               │
│ last_name                                │
│ is_staff (T/F)                           │
│ is_superuser (T/F)                       │
│ date_joined                              │
└────────┬─────────────────────────────────┘
         │ (OneToOne)
         │
┌────────▼──────────────────────────────────┐
│       Student Table                      │
├───────────────────────────────────────────┤
│ id (PK)                                   │
│ user_id (FK, UNIQUE)                      │
│ phone                                     │
│ class_name                                │
│ qr_code (ImageField → media/qr_codes/)   │
│ created_at                                │
│ updated_at                                │
└────────┬──────────────────────────────────┘
         │ (ForeignKey)
         │
┌────────▼──────────────────────────────────┐
│     Attendance Table                     │
├───────────────────────────────────────────┤
│ id (PK)                                   │
│ student_id (FK)                           │
│ date                                      │
│ time                                      │
│ status (present/absent/late)              │
│ created_at                                │
│ UNIQUE(student_id, date)                  │
└───────────────────────────────────────────┘
```

---

## QR Code Data Format & Parsing

```
QR Code Generation (Backend):
─────────────────────────────
Student Object
    │
    ├─ user.id = 5
    ├─ user.first_name = "John"
    ├─ user.last_name = "Doe"
    └─ class_name = "10-A"
    │
    ▼
Generate QR Data:
    5|John Doe|10-A
    │
    ▼
Encode to QR Image (PNG)
    │
    ▼
Save to: media/qr_codes/qr_code_5_xxxxx.png
    │
    ▼
Display on Student Dashboard


QR Code Scanning (Frontend):
──────────────────────────────
Scan QR Code with Camera
    │
    ▼
ZXing.js Library Decodes
    │
    ▼
Extract Text: "5|John Doe|10-A"
    │
    ▼
Send to Backend API: /api/save-attendance/
    {qr_data: "5|John Doe|10-A"}
    │
    ▼
Backend Parsing:
    ├─ Split by '|'
    ├─ parts[0] = student_id (5)
    ├─ parts[1] = name ("John Doe")
    └─ parts[2] = class ("10-A")
    │
    ▼
Validation:
    ├─ Check: Student exists with id=5
    ├─ Check: Name matches student.user.name
    ├─ Check: Class matches student.class_name
    └─ Check: No duplicate today
    │
    ▼
Save Attendance Record
    Attendance(
        student_id=5,
        date=2024-11-15,
        time=14:30:45,
        status='present'
    )
    │
    ▼
Return Success: ✓ Attendance Marked
```

---

## API Request-Response Cycle

```
SAVE ATTENDANCE API
═══════════════════

CLIENT REQUEST:
──────────────
POST /api/save-attendance/ HTTP/1.1
Content-Type: application/json
X-CSRFToken: abc123...

{
    "qr_data": "5|John Doe|10-A"
}

        │
        ▼

SERVER PROCESSING:
─────────────────
1. Verify CSRF token
2. Parse JSON payload
3. Extract qr_data
4. Split by '|'
5. Validate all parts
6. Query Student DB
7. Check attendance today
8. Create Attendance record
9. Generate response

        │
        ▼

SERVER RESPONSE:
───────────────
HTTP/1.1 200 OK
Content-Type: application/json

{
    "success": true,
    "message": "Attendance marked for John Doe",
    "student_name": "John Doe",
    "student_class": "10-A"
}

        │
        ▼

CLIENT HANDLING:
───────────────
JavaScript receives response
    │
    ├─ Check: response.success
    ├─ Update UI: Show success message
    ├─ Display: Student name & class
    ├─ Reset scanner: Continue scanning
    └─ Auto-hide: Message after 3 seconds
```

---

## Template Inheritance Structure

```
base.html (Base Template)
│
├─▶ Navbar (if authenticated)
├─▶ Block: content
├─▶ Block: extra_css
├─▶ Block: extra_js
└─▶ Footer
    │
    ├──┬─▶ home.html
    │  │   ├─ Extends: base.html
    │  │   └─ Content: Home cards
    │  │
    │  ├──┬─▶ student_login.html
    │  │  │   ├─ Extends: base.html
    │  │  │   └─ Content: Login form
    │  │  │
    │  ├──┬─▶ student_register.html
    │  │  │   ├─ Extends: base.html
    │  │  │   └─ Content: Registration form
    │  │  │
    │  ├──┬─▶ student_dashboard.html
    │  │  │   ├─ Extends: base.html
    │  │  │   └─ Content: QR code + Attendance table
    │  │  │
    │  ├──┬─▶ admin_login.html
    │  │  │   ├─ Extends: base.html
    │  │  │   └─ Content: Admin login form
    │  │  │
    │  ├──┬─▶ admin_scanner.html
    │  │  │   ├─ Extends: base.html
    │  │  │   ├─ Content: Video tag + Scanner UI
    │  │  │   ├─ Extra CSS: Scanner styles
    │  │  │   └─ Extra JS: ZXing.js + Scanner logic
    │  │  │
    │  └──┬─▶ admin_report.html
    │     ├─ Extends: base.html
    │     └─ Content: Report filters + Table
    │
    └─── All templates include:
         ├─ CSRF tokens on forms
         ├─ Bootstrap classes
         ├─ Responsive design
         └─ Error/Success messages
```

---

## Authentication & Authorization Flow

```
User Login Process:
═══════════════════

┌─────────────────┐
│  Anonymous User │
└────────┬────────┘
         │
         ▼
    Visits: /student/login/
         │
         ▼
    Django View:
    student_login()
         │
    ├─ Method: GET
    │   │
    │   └─▶ Render: student_login.html
    │       (empty form)
    │
    └─ Method: POST
        │
        ├─▶ Get credentials from form
        │   (email, password)
        │
        ├─▶ Find User by email
        │
        ├─▶ Authenticate password
        │
        ├─ ✓ Correct password
        │   │
        │   ├─▶ Create session
        │   ├─▶ Set session cookie
        │   └─▶ Redirect: /student/dashboard/
        │
        └─ ✗ Wrong password
            │
            └─▶ Re-render form with error


PROTECTED PAGES:
════════════════

@login_required decorator:
    │
    ├─ User is authenticated?
    │   │
    │   ├─ ✓ YES: Allow access to view
    │   │   │
    │   │   └─▶ Render protected page
    │   │
    │   └─ ✗ NO: Redirect to login
    │       (redirect to: LOGIN_URL)


STAFF-ONLY PAGES:
═════════════════

Admin views check:
    │
    ├─ user.is_staff == True?
    │   │
    │   ├─ ✓ YES: Allow access
    │   │   │
    │   │   └─▶ Render admin page
    │   │
    │   └─ ✗ NO: Redirect to login
```

---

## File Upload & Storage

```
QR Code Generation & Storage:
══════════════════════════════

Student Created:
    │
    ▼
Call: student.generate_qr_code()
    │
    ├─ Generate image in memory
    │   (PIL Image object)
    │
    ├─ Convert to PNG bytes
    │
    ├─ Create filename:
    │   qr_code_{student_id}_{timestamp}.png
    │
    ├─ Save to media folder:
    │   media/qr_codes/qr_code_5_1234567890.png
    │
    └─▶ Serve via /media/ URL:
        URL: /media/qr_codes/qr_code_5_1234567890.png
        │
        ▼
    Display in HTML:
    <img src="{{student.qr_code.url}}" alt="QR Code">
```

---

## Error Handling Flow

```
Invalid QR Scan:
═════════════════

QR Detected: "INVALID|DATA|FORMAT"
    │
    ▼
Send to API: /api/save-attendance/
    │
    ▼
Backend Processing:
    │
    ├─ Try: Parse JSON
    │   │
    │   └─ ✓ Success
    │
    ├─ Extract: qr_data
    │
    ├─ Try: Split by '|'
    │   │
    │   └─ Check: len(parts) == 3?
    │       │
    │       ├─ ✗ NO
    │       │   │
    │       │   └─▶ Return Error:
    │       │       {success: false,
    │       │        message: "Invalid QR format"}
    │       │
    │       └─ ✓ YES
    │           │
    │           └─▶ Continue validation
    │
    ├─ Try: Query Student
    │   │
    │   ├─ ✗ NOT FOUND
    │   │   │
    │   │   └─▶ Return Error:
    │   │       {success: false,
    │   │        message: "Student not found"}
    │   │
    │   └─ ✓ FOUND
    │       │
    │       └─▶ Validate data match
    │
    ├─ Check: Name matches?
    │   │
    │   ├─ ✗ NO MATCH
    │   │   │
    │   │   └─▶ Return Error:
    │   │       {success: false,
    │   │        message: "QR data mismatch"}
    │   │
    │   └─ ✓ MATCH
    │       │
    │       └─▶ Check: Class matches?
    │
    └─▶ All validations passed
        │
        ▼
    Save Attendance ✓
        │
        ▼
    Return Success:
    {success: true,
     message: "Attendance marked..."}


FRONTEND ERROR HANDLING:
═════════════════════════

Response received:
    │
    ├─ response.success == true?
    │   │
    │   ├─ ✓ YES
    │   │   │
    │   │   └─▶ Show Green Badge: ✓ Success
    │   │       Display: Student name
    │   │       Auto-hide: 3 seconds
    │   │
    │   └─ ✗ NO
    │       │
    │       └─▶ Show Red Badge: ✗ Error
    │           Display: error message
    │           Auto-hide: 5 seconds
    │
    └─▶ Continue scanning
```

---

This architecture ensures:
- ✅ Clean separation of concerns
- ✅ Secure authentication
- ✅ Proper error handling
- ✅ Real-time feedback
- ✅ Data validation
- ✅ Responsive UI
- ✅ Scalable design
