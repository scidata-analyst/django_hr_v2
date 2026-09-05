from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def employee(request):
    return render(request, 'pages/employee.html')

def employee_detail(request, id):
    return render(request, 'pages/employee.html', {'id': id})

def employee_create(request):
    return render(request, 'pages/employee.html')

def employee_update(request, id):
    return render(request, 'pages/employee.html', {'id': id})

def employee_delete(request, id):
    return render(request, 'pages/employee.html', {'id': id})