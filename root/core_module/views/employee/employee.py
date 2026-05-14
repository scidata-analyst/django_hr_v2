from django.shortcuts import render

# Create your views here.
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