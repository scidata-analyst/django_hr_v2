from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

@ensure_csrf_cookie
@login_required
def payroll(request):
    return render(request, 'pages/payroll.html')