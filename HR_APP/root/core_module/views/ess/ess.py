from django.shortcuts import render

# Create your views here.
def ess(request):
    return render(request, 'pages/ess.html')