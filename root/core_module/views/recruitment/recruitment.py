from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def recruitment(request):
    return render(request, 'pages/recruitment.html')