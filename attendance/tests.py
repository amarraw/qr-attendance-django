"""
Tests for the attendance app.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from attendance.models import Student, Attendance
from datetime import datetime, date


class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_student_creation(self):
        student = Student.objects.create(
            user=self.user,
            phone='9876543210',
            class_name='10-A'
        )
        self.assertTrue(student.qr_code)
        self.assertEqual(str(student), 'Test User - 10-A')

    def test_qr_code_generation(self):
        student = Student.objects.create(
            user=self.user,
            phone='9876543210',
            class_name='10-A'
        )
        self.assertIsNotNone(student.qr_code)
        self.assertTrue(student.qr_code.name.startswith('qr_code_'))


class AttendanceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.student = Student.objects.create(
            user=self.user,
            phone='9876543210',
            class_name='10-A'
        )

    def test_attendance_creation(self):
        attendance = Attendance.objects.create(
            student=self.student,
            date=date.today(),
            time=datetime.now().time(),
            status='present'
        )
        self.assertEqual(attendance.status, 'present')
        self.assertEqual(attendance.student, self.student)

    def test_unique_attendance_per_day(self):
        """Test that only one attendance per student per day is allowed"""
        Attendance.objects.create(
            student=self.student,
            date=date.today(),
            time=datetime.now().time(),
            status='present'
        )
        # This should fail due to unique_together constraint
        with self.assertRaises(Exception):
            Attendance.objects.create(
                student=self.student,
                date=date.today(),
                time=datetime.now().time(),
                status='present'
            )
