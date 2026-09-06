from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def ess(request):
    return render(request, 'pages/ess.html')