from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


class EssController:
    template_name = 'pages/ess.html'
    route_name = 'ess'

    @staticmethod
    def all(request):
        return render(request, EssController.template_name)

    @staticmethod
    def index(request):
        return render(request, EssController.template_name)

    @staticmethod
    def create(request):
        return render(request, EssController.template_name)

    @staticmethod
    @require_http_methods(["POST"])
    def store(request):
        return redirect(EssController.route_name)

    @staticmethod
    def show(request, id):
        return render(request, EssController.template_name, {'id': id})

    @staticmethod
    def edit(request, id):
        return render(request, EssController.template_name, {'id': id})

    @staticmethod
    @require_http_methods(["POST", "PUT", "PATCH"])
    def update(request, id):
        return redirect(EssController.route_name)

    @staticmethod
    @require_http_methods(["POST", "DELETE"])
    def destroy(request, id):
        return redirect(EssController.route_name)


index = EssController.index
all = EssController.all
create = EssController.create
store = EssController.store
show = EssController.show
edit = EssController.edit
update = EssController.update
destroy = EssController.destroy
