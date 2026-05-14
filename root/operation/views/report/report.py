from django.shortcuts import render

# Create your views here.
def report(request):
    # Template name is plural in this project (`reports.html`)
    return render(request, 'pages/reports.html')