from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


class PayrollController:
    template_name = 'pages/payroll.html'
    route_name = 'payroll'

    @staticmethod
    def all(request):
        return render(request, PayrollController.template_name)

    @staticmethod
    def index(request):
        return render(request, PayrollController.template_name)

    @staticmethod
    def create(request):
        return render(request, PayrollController.template_name)

    @staticmethod
    @require_http_methods(["POST"])
    def store(request):
        return redirect(PayrollController.route_name)

    @staticmethod
    def show(request, id):
        return render(request, PayrollController.template_name, {'id': id})

    @staticmethod
    def edit(request, id):
        return render(request, PayrollController.template_name, {'id': id})

    @staticmethod
    @require_http_methods(["POST", "PUT", "PATCH"])
    def update(request, id):
        return redirect(PayrollController.route_name)

    @staticmethod
    @require_http_methods(["POST", "DELETE"])
    def destroy(request, id):
        return redirect(PayrollController.route_name)


index = PayrollController.index
all = PayrollController.all
create = PayrollController.create
store = PayrollController.store
show = PayrollController.show
edit = PayrollController.edit
update = PayrollController.update
destroy = PayrollController.destroy
