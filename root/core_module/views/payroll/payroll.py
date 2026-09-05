from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def payroll(request):
    return render(request, 'pages/payroll.html')