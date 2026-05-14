from django.shortcuts import render

# Create your views here.
def branding(request):
    return render(request, 'pages/branding.html')