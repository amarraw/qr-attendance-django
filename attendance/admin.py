"""
Django admin configuration for attendance app.
"""
from django.contrib import admin
from .models import Student, Attendance


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_name', 'phone', 'created_at')
    list_filter = ('class_name', 'created_at')
    search_fields = ('user__username', 'user__email', 'class_name')
    readonly_fields = ('qr_code', 'created_at', 'updated_at')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'time', 'status')
    list_filter = ('date', 'status', 'student__class_name')
    search_fields = ('student__user__username', 'student__user__email')
    readonly_fields = ('created_at',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('student', 'date')
        return self.readonly_fields
