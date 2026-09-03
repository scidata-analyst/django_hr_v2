from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


class AttendanceController:
    template_name = 'pages/attendance.html'
    route_name = 'attendance'

    @staticmethod
    def all(request):
        return render(request, AttendanceController.template_name)

    @staticmethod
    def index(request):
        return render(request, AttendanceController.template_name)

    @staticmethod
    def create(request):
        return render(request, AttendanceController.template_name)

    @staticmethod
    @require_http_methods(["POST"])
    def store(request):
        return redirect(AttendanceController.route_name)

    @staticmethod
    def show(request, id):
        return render(request, AttendanceController.template_name, {'id': id})

    @staticmethod
    def edit(request, id):
        return render(request, AttendanceController.template_name, {'id': id})

    @staticmethod
    @require_http_methods(["POST", "PUT", "PATCH"])
    def update(request, id):
        return redirect(AttendanceController.route_name)

    @staticmethod
    @require_http_methods(["POST", "DELETE"])
    def destroy(request, id):
        return redirect(AttendanceController.route_name)


index = AttendanceController.index
all = AttendanceController.all
create = AttendanceController.create
store = AttendanceController.store
show = AttendanceController.show
edit = AttendanceController.edit
update = AttendanceController.update
destroy = AttendanceController.destroy
