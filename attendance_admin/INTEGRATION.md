Add the attendance_admin URLs to the project `qr_attendance/urls.py` to expose the admin panel under `/adminpanel/`.

Open `qr_attendance/urls.py` and add the following import and include:

from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpanel/', include('attendance_admin.urls', namespace='attendance_admin')),
    path('', include('attendance.urls')),
]

Notes:
 Ensure `attendance_admin` is added to `INSTALLED_APPS` in `qr_attendance/settings.py` if you want Django to notice it (not strictly necessary for templates/static when using app directories, but recommended):

INSTALLED_APPS = [
    # ... existing apps ...
    'attendance_admin',
]

- Restart the server after updating `INSTALLED_APPS` or `urls.py`.
- The scanner page registers a service worker and uses ZXing; ensure the static files are served in development (DEBUG=True) which is the default in settings.
