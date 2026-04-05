from django.shortcuts import render

# Create your views here.
def payroll(request):
    return render(request, 'pages/payroll.html')