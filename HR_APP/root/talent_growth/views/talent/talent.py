from django.shortcuts import render

# Create your views here.
def talent(request):
    return render(request, 'pages/talent.html')