from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

@ensure_csrf_cookie
@login_required
def employee(request):
    return render(request, 'pages/employee.html')

@login_required
def employee_detail(request, id):
    return render(request, 'pages/employee.html', {'id': id})

@login_required
def employee_create(request):
    return render(request, 'pages/employee.html')

@login_required
def employee_update(request, id):
    return render(request, 'pages/employee.html', {'id': id})

@login_required
def employee_delete(request, id):
    return render(request, 'pages/employee.html', {'id': id})