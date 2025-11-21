{% load static %}
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Admin Panel{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{% static 'adminpanel/style.css' %}">
    <link rel="manifest" href="{% static 'adminpanel/manifest.json' %}">
    {% block extra_head %}{% endblock %}
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">QR Admin Panel</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        {% if user.is_authenticated and user.is_staff %}
        <li class="nav-item"><a class="nav-link" href="{% url 'attendance_admin:dashboard' %}">Dashboard</a></li>
        <li class="nav-item"><a class="nav-link" href="{% url 'attendance_admin:scanner' %}">Scanner</a></li>
        <li class="nav-item"><a class="nav-link" href="{% url 'attendance_admin:reports' %}">Reports</a></li>
        <li class="nav-item"><a class="nav-link" href="/admin/">Django Admin</a></li>
        <li class="nav-item"><a class="nav-link" href="/adminpanel/logout/">Logout</a></li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>

<div class="container mt-4">
    {% block content %}{% endblock %}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
{% block extra_js %}{% endblock %}
</body>
</html>{% extends 'adminpanel/base.html' %}
{% block title %}Admin Login{% endblock %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-5">
    <div class="card">
      <div class="card-body">
        <h3 class="card-title text-center">Admin Login</h3>
        {% if error %}
        <div class="alert alert-danger">{{ error }}</div>
        {% endif %}
        <form method="post" action="">
          {% csrf_token %}
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" name="username" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" name="password" class="form-control" required>
          </div>
          <button class="btn btn-primary w-100">Login</button>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}{% extends 'adminpanel/base.html' %}
{% block title %}Admin Login{% endblock %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-5">
    <div class="card">
      <div class="card-body">
        <h3 class="card-title text-center">Admin Login</h3>
        {% if error %}
        <div class="alert alert-danger">{{ error }}</div>
        {% endif %}
        <form method="post" action="">
          {% csrf_token %}
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" name="username" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" name="password" class="form-control" required>
          </div>
          <button class="btn btn-primary w-100">Login</button>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}{% extends 'adminpanel/base.html' %}
{% block title %}Admin Login{% endblock %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-5">
    <div class="card">
      <div class="card-body">
        <h3 class="card-title text-center">Admin Login</h3>
        {% if error %}
        <div class="alert alert-danger">{{ error }}</div>
        {% endif %}
        <form method="post" action="">
          {% csrf_token %}
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" name="username" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" name="password" class="form-control" required>
          </div>
          <button class="btn btn-primary w-100">Login</button>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}
