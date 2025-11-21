import csv
import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from attendance.models import Student, Attendance


# Helper decorator: ensure staff user
def staff_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('attendance_admin:login')
        if not request.user.is_staff:
            return HttpResponseForbidden('Forbidden: staff only')
        return view_func(request, *args, **kwargs)
    _wrapped.__name__ = view_func.__name__
    return _wrapped


def adminpanel_login(request):
    """Custom admin login (not Django admin)."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('attendance_admin:dashboard')
        else:
            return render(request, 'adminpanel/login.html', {'error': 'Invalid credentials or not an admin'})
    return render(request, 'adminpanel/login.html')


def adminpanel_logout(request):
    """Logout admin user and redirect to adminpanel login."""
    logout(request)
    return redirect('attendance_admin:login')
import csv
import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from attendance.models import Student, Attendance


# Helper decorator: ensure staff user
def staff_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('attendance_admin:login')
        if not request.user.is_staff:
            return HttpResponseForbidden('Forbidden: staff only')
        return view_func(request, *args, **kwargs)
    _wrapped.__name__ = view_func.__name__
    return _wrapped


def adminpanel_login(request):
    """Custom admin login (not Django admin)."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('attendance_admin:dashboard')
        else:
            return render(request, 'adminpanel/login.html', {'error': 'Invalid credentials or not an admin'})
    return render(request, 'adminpanel/login.html')


def adminpanel_logout(request):
    """Logout admin user and redirect to adminpanel login."""
    logout(request)
    return redirect('attendance_admin:login')


@login_required(login_url='attendance_admin:login')
@staff_required
def dashboard(request):
    return render(request, 'adminpanel/dashboard.html')


@login_required(login_url='attendance_admin:login')
@staff_required
def scanner(request):
    return render(request, 'adminpanel/scanner.html')


@login_required(login_url='attendance_admin:login')
@staff_required
@require_http_methods(["POST"])
def save_attendance(request):
    """Save attendance from scanner POST (expects JSON {"qr": "..."})."""
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    qr = data.get('qr', '')
    parts = qr.split('|')
    if len(parts) != 3:
        return JsonResponse({'success': False, 'message': 'Invalid QR format'}, status=400)

    student_id_str, name, class_name = parts
    try:
        student_id = int(student_id_str)
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Invalid student id'}, status=400)

    try:
        student = Student.objects.get(user_id=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Student not found'}, status=404)

    # Validate name and class
    student_full_name = student.user.get_full_name() or student.user.username
    if name != student_full_name or class_name != student.class_name:
        return JsonResponse({'success': False, 'message': 'QR data mismatch with student profile'}, status=400)

    today = datetime.now().date()
    now_time = datetime.now().time()

    # Prevent duplicates: unique per student+date
    attendance, created = Attendance.objects.get_or_create(
        student=student,
        date=today,
        defaults={'time': now_time, 'status': 'Present'}
    )

    if not created:
        # Update time/status if already exists
        attendance.time = now_time
        attendance.status = 'Present'
        attendance.save()

    # Try to return student photo URL if available
    photo_url = ''
    try:
        if student.qr_code:
            photo_url = student.qr_code.url
    except Exception:
        photo_url = ''

    return JsonResponse({
        'success': True,
        'message': 'Attendance saved',
        'student_name': student_full_name,
        'class': student.class_name,
        'time': attendance.time.strftime('%H:%M:%S'),
        'photo_url': photo_url,
    })


@login_required(login_url='attendance_admin:login')
@staff_required
def reports(request):
    # Filters
    date_filter = request.GET.get('date')
    class_filter = request.GET.get('class')

    attendances = Attendance.objects.select_related('student__user').all().order_by('-date', '-time')

    if date_filter:
        try:
            date_obj = datetime.fromisoformat(date_filter).date()
            attendances = attendances.filter(date=date_obj)
        except ValueError:
            pass

    if class_filter:
        attendances = attendances.filter(student__class_name=class_filter)

    classes = Student.objects.values_list('class_name', flat=True).distinct()

    return render(request, 'adminpanel/reports.html', {
        'attendances': attendances,
        'classes': classes,
        'date_filter': date_filter,
        'class_filter': class_filter,
    })


@login_required(login_url='attendance_admin:login')
@staff_required
def export_csv(request):
    date_filter = request.GET.get('date')
    class_filter = request.GET.get('class')

    attendances = Attendance.objects.select_related('student__user').all().order_by('-date', '-time')

    if date_filter:
        try:
            date_obj = datetime.fromisoformat(date_filter).date()
            attendances = attendances.filter(date=date_obj)
        except ValueError:
            pass

    if class_filter:
        attendances = attendances.filter(student__class_name=class_filter)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Student Name', 'Class', 'Date', 'Time', 'Status'])

    for att in attendances:
        writer.writerow([
            att.student.user.id,
            att.student.user.get_full_name() or att.student.user.username,
            att.student.class_name,
            att.date,
            att.time.strftime('%H:%M:%S'),
            att.status,
        ])

    return response
