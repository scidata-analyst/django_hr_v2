from django.shortcuts import render

# Create your views here.
def engagement(request):
    return render(request, 'pages/engagement.html')