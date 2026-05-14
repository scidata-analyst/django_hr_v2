from django.shortcuts import render

# Create your views here.
def recruitment(request):
    return render(request, 'pages/recruitment.html')