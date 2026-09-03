from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


class RecruitmentController:
    template_name = 'pages/recruitment.html'
    route_name = 'recruitment'

    @staticmethod
    def all(request):
        return render(request, RecruitmentController.template_name)

    @staticmethod
    def index(request):
        return render(request, RecruitmentController.template_name)

    @staticmethod
    def create(request):
        return render(request, RecruitmentController.template_name)

    @staticmethod
    @require_http_methods(["POST"])
    def store(request):
        return redirect(RecruitmentController.route_name)

    @staticmethod
    def show(request, id):
        return render(request, RecruitmentController.template_name, {'id': id})

    @staticmethod
    def edit(request, id):
        return render(request, RecruitmentController.template_name, {'id': id})

    @staticmethod
    @require_http_methods(["POST", "PUT", "PATCH"])
    def update(request, id):
        return redirect(RecruitmentController.route_name)

    @staticmethod
    @require_http_methods(["POST", "DELETE"])
    def destroy(request, id):
        return redirect(RecruitmentController.route_name)


index = RecruitmentController.index
all = RecruitmentController.all
create = RecruitmentController.create
store = RecruitmentController.store
show = RecruitmentController.show
edit = RecruitmentController.edit
update = RecruitmentController.update
destroy = RecruitmentController.destroy
