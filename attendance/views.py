"""
Views for the attendance app.
"""
import json
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
import csv
from django.http import HttpResponse

from .models import Student, Attendance
from .forms import StudentLoginForm, StudentRegistrationForm, AdminLoginForm


def home(request):
    """Home page with links to student and admin login."""
    return render(request, 'home.html')


# ==================== STUDENT VIEWS ====================

def student_login(request):
    """Student login view."""
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Find user by email
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('student_dashboard')
                else:
                    form.add_error(None, 'Invalid email or password.')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = StudentLoginForm()
    
    return render(request, 'student_login.html', {'form': form})


def student_register(request):
    """Student registration view."""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create student profile
            student = form.save(commit=False)
            student.user = user
            student.save()
            student.generate_qr_code()

            return redirect('student_login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'student_register.html', {'form': form})


@login_required(login_url='student_login')
def student_dashboard(request):
    """Student dashboard showing their QR code."""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('student_login')
    
    # Get recent attendance
    recent_attendance = student.attendances.all()[:10]
    
    context = {
        'student': student,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'student_dashboard.html', context)


def student_logout(request):
    """Student logout view."""
    logout(request)
    return redirect('student_login')


# ==================== ADMIN VIEWS ====================

def admin_login(request):
    """Admin login view."""
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_scanner')
            else:
                form.add_error(None, 'Invalid credentials or not an admin.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin_login.html', {'form': form})


@login_required(login_url='admin_login')
def admin_scanner(request):
    """Admin QR code scanner page."""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    return render(request, 'admin_scanner.html')


@login_required(login_url='admin_login')
def admin_logout(request):
    """Admin logout view."""
    logout(request)
    return redirect('admin_login')


@login_required(login_url='admin_login')
def admin_report(request):
    """Admin attendance report page."""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    # Get all attendances
    attendances = Attendance.objects.all().order_by('-date', '-time')
    
    # Filter by date if provided
    date_filter = request.GET.get('date')
    if date_filter:
        attendances = attendances.filter(date=date_filter)
    
    # Filter by class if provided
    class_filter = request.GET.get('class')
    if class_filter:
        attendances = attendances.filter(student__class_name=class_filter)
    
    # Get unique classes for filter dropdown
    classes = Student.objects.values_list('class_name', flat=True).distinct()
    
    context = {
        'attendances': attendances,
        'classes': classes,
        'date_filter': date_filter,
        'class_filter': class_filter,
    }
    return render(request, 'admin_report.html', context)


@login_required(login_url='admin_login')
def download_attendance_csv(request):
    """Download attendance report as CSV."""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    attendances = Attendance.objects.all().order_by('-date', '-time')
    
    # Filter by date if provided
    date_filter = request.GET.get('date')
    if date_filter:
        attendances = attendances.filter(date=date_filter)
    
    # Filter by class if provided
    class_filter = request.GET.get('class')
    if class_filter:
        attendances = attendances.filter(student__class_name=class_filter)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Student Name', 'Class', 'Date', 'Time', 'Status'])
    
    for attendance in attendances:
        writer.writerow([
            attendance.student.user.id,
            attendance.student.user.get_full_name() or attendance.student.user.username,
            attendance.student.class_name,
            attendance.date,
            attendance.time,
            attendance.status,
        ])
    
    return response


# ==================== API ENDPOINTS ====================

@require_http_methods(["POST"])
@csrf_exempt
def save_attendance(request):
    """API endpoint to save attendance from scanned QR code."""
    try:
        data = json.loads(request.body)
        qr_data = data.get('qr_data', '')
        
        # Parse QR data: student_id|name|class_name
        parts = qr_data.split('|')
        if len(parts) != 3:
            return JsonResponse({
                'success': False,
                'message': 'Invalid QR code format'
            }, status=400)
        
        student_id, name, class_name = parts
        
        try:
            student_id = int(student_id)
            student = Student.objects.get(user_id=student_id)
        except (ValueError, Student.DoesNotExist):
            return JsonResponse({
                'success': False,
                'message': 'Student not found'
            }, status=404)
        
        # Validate QR data matches student
        student_full_name = student.user.get_full_name() or student.user.username
        if name != student_full_name or class_name != student.class_name:
            return JsonResponse({
                'success': False,
                'message': 'QR code data does not match student profile'
            }, status=400)
        
        # Create or update attendance
        today = datetime.now().date()
        now = datetime.now().time()
        
        attendance, created = Attendance.objects.get_or_create(
            student=student,
            date=today,
            defaults={'time': now, 'status': 'present'}
        )
        
        if not created:
            # If attendance already exists, just update status
            attendance.status = 'present'
            attendance.time = now
            attendance.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Attendance marked for {student_full_name}',
            'student_name': student_full_name,
            'student_class': class_name,
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def check_attendance_exists(request):
    """Check if attendance already exists for today."""
    student_id = request.GET.get('student_id')
    
    try:
        student = Student.objects.get(user_id=student_id)
        today = datetime.now().date()
        
        exists = Attendance.objects.filter(
            student=student,
            date=today
        ).exists()
        
        return JsonResponse({
            'exists': exists
        })
    except Student.DoesNotExist:
        return JsonResponse({
            'exists': False
        })
