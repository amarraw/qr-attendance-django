"""
URL configuration for attendance app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Student URLs
    path('student/login/', views.student_login, name='student_login'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/logout/', views.student_logout, name='student_logout'),
    
    # Admin URLs
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/scanner/', views.admin_scanner, name='admin_scanner'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/report/', views.admin_report, name='admin_report'),
    path('admin/download-csv/', views.download_attendance_csv, name='download_csv'),
    
    # API endpoints
    path('api/save-attendance/', views.save_attendance, name='save_attendance'),
    path('api/check-attendance/', views.check_attendance_exists, name='check_attendance'),
]
