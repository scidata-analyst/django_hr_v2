from django.shortcuts import render

# Create your views here.
def global_view(request):
    return render(request, 'pages/global.html')