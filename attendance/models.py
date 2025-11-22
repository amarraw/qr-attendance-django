"""
Models for the attendance app.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import qrcode
import io
from datetime import datetime


class Student(models.Model):
    """Student model linked to Django User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    class_name = models.CharField(max_length=50)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    EROOOOOORRRRR
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.class_name}"

    def generate_qr_code(self):
        """Generate QR code containing student_id|name|class_name."""
        qr_data = f"{self.user.id}|{self.user.get_full_name() or self.user.username}|{self.class_name}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save to model
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        filename = f"qr_code_{self.user.id}_{datetime.now().timestamp()}.png"
        self.qr_code.save(filename, ContentFile(img_io.getvalue()), save=True)

        return self.qr_code

    def save(self, *args, **kwargs):
        """Override save to generate QR code on creation."""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Generate QR code only if it doesn't exist
        if is_new and not self.qr_code:
            self.generate_qr_code()


class Attendance(models.Model):
    """Attendance model to track student attendance."""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student} - {self.date} ({self.status})"
