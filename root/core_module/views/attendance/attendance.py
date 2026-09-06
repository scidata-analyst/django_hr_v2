from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

@ensure_csrf_cookie
@login_required
def attendance(request):
    return render(request, 'pages/attendance.html')