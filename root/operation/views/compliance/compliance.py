from django.shortcuts import render

# Create your views here.
def compliance(request):
    return render(request, 'pages/compliance.html')