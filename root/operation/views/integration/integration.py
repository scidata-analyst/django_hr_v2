from django.shortcuts import render

# Create your views here.
def integration(request):
    # Template name is plural in this project (`integrations.html`)
    return render(request, 'pages/integrations.html')