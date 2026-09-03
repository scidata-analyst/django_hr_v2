from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


class OnboardingController:
    template_name = 'pages/onboarding.html'
    route_name = 'onboarding'

    @staticmethod
    def all(request):
        return render(request, OnboardingController.template_name)

    @staticmethod
    def index(request):
        return render(request, OnboardingController.template_name)

    @staticmethod
    def create(request):
        return render(request, OnboardingController.template_name)

    @staticmethod
    @require_http_methods(["POST"])
    def store(request):
        return redirect(OnboardingController.route_name)

    @staticmethod
    def show(request, id):
        return render(request, OnboardingController.template_name, {'id': id})

    @staticmethod
    def edit(request, id):
        return render(request, OnboardingController.template_name, {'id': id})

    @staticmethod
    @require_http_methods(["POST", "PUT", "PATCH"])
    def update(request, id):
        return redirect(OnboardingController.route_name)

    @staticmethod
    @require_http_methods(["POST", "DELETE"])
    def destroy(request, id):
        return redirect(OnboardingController.route_name)


index = OnboardingController.index
all = OnboardingController.all
create = OnboardingController.create
store = OnboardingController.store
show = OnboardingController.show
edit = OnboardingController.edit
update = OnboardingController.update
destroy = OnboardingController.destroy
