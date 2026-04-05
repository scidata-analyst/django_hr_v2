from django.shortcuts import render

# Create your views here.
def onboarding(request):
    return render(request, 'pages/onboarding.html')