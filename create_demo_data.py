# QR Attendance System - Demo Data Script

from django.contrib.auth.models import User
from attendance.models import Student, Attendance
from datetime import datetime, timedelta
import os

def create_demo_data():
    """Create demo students and attendance records for testing"""
    
    print("Creating demo data...")
    
    # Create demo students
    demo_students = [
        {
            'username': 'student1',
            'email': 'student1@example.com',
            'first_name': 'Arav',
            'last_name': 'Sharma',
            'password': 'student123',
            'phone': '9876543210',
            'class_name': '10-A'
        },
        {
            'username': 'student2',
            'email': 'student2@example.com',
            'first_name': 'Priya',
            'last_name': 'Singh',
            'password': 'student123',
            'phone': '9876543211',
            'class_name': '10-A'
        },
        {
            'username': 'student3',
            'email': 'student3@example.com',
            'first_name': 'Rohan',
            'last_name': 'Kumar',
            'password': 'student123',
            'phone': '9876543212',
            'class_name': '10-B'
        },
    ]
    
    for student_data in demo_students:
        # Create user
        user, created = User.objects.get_or_create(
            username=student_data['username'],
            defaults={
                'email': student_data['email'],
                'first_name': student_data['first_name'],
                'last_name': student_data['last_name'],
            }
        )
        
        if created:
            user.set_password(student_data['password'])
            user.save()
        
        # Create student profile
        student, created = Student.objects.get_or_create(
            user=user,
            defaults={
                'phone': student_data['phone'],
                'class_name': student_data['class_name'],
            }
        )
        
        if created:
            student.generate_qr_code()
            print(f"✓ Created student: {user.get_full_name()}")
        
        # Create attendance records for last 10 days
        for i in range(10):
            date = datetime.now().date() - timedelta(days=i)
            time = datetime.strptime("09:00:00", "%H:%M:%S").time()
            
            Attendance.objects.get_or_create(
                student=student,
                date=date,
                defaults={
                    'time': time,
                    'status': 'present' if i % 3 != 0 else 'absent'
                }
            )
        
        print(f"✓ Created attendance records for {user.get_full_name()}")
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ Created admin user (username: admin, password: admin123)")
    
    print("\nDemo data created successfully!")
    print("\nYou can now login with:")
    print("  Student: student1 / student123")
    print("  Admin: admin / admin123")

if __name__ == '__main__':
    create_demo_data()
