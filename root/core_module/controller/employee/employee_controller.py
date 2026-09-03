from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


class EmployeeController:
    template_name = 'pages/employee.html'
    route_name = 'employee'

    @staticmethod
    def all(request):
        return render(request, EmployeeController.template_name)

    @staticmethod
    def index(request):
        return render(request, EmployeeController.template_name)

    @staticmethod
    def create(request):
        return render(request, EmployeeController.template_name)

    @staticmethod
    @require_http_methods(["POST"])
    def store(request):
        return redirect(EmployeeController.route_name)

    @staticmethod
    def show(request, id):
        return render(request, EmployeeController.template_name, {'id': id})

    @staticmethod
    def edit(request, id):
        return render(request, EmployeeController.template_name, {'id': id})

    @staticmethod
    @require_http_methods(["POST", "PUT", "PATCH"])
    def update(request, id):
        return redirect(EmployeeController.route_name)

    @staticmethod
    @require_http_methods(["POST", "DELETE"])
    def destroy(request, id):
        return redirect(EmployeeController.route_name)


index = EmployeeController.index
all = EmployeeController.all
create = EmployeeController.create
store = EmployeeController.store
show = EmployeeController.show
edit = EmployeeController.edit
update = EmployeeController.update
destroy = EmployeeController.destroy
