from django.urls import path
from . import views

app_name = 'attendance_admin'

urlpatterns = [
    path('login/', views.adminpanel_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('scanner/', views.scanner, name='scanner'),
    path('save-attendance/', views.save_attendance, name='save_attendance'),
    path('reports/', views.reports, name='reports'),
    path('reports/export/', views.export_csv, name='export_csv'),
    path('logout/', views.adminpanel_logout, name='logout'),
]
