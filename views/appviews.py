from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from ..forms.forms import LeaveRequestForm

from ..models.models import Employee, LeaveRequest, LeaveType


class LeaveRequestApproveView(CreateView):
    model = LeaveRequest

    def get(self, request, *args, **kwargs):
        ...


class LeaveRequestDeleteView(DeleteView):
    model = LeaveRequest


class LeaveRequestListView(ListView):
    template_name = "leavemanager/list.html"

    def get_queryset(self):
        queryset = LeaveRequest.objects.all()
        if self.request.user.is_superuser:
            return queryset
        employee = Employee.objects.get_or_none(user_id=self.request.user.id)
        employees = list(Employee.objects.filter(reporting_manager=employee))
        return queryset.filter(employee__in=[*employees, employee])


class LeaveRequestCreateView(TemplateView):
    form_class = LeaveRequestForm
    model = LeaveRequest
    template_name = "leavemanager/create.html"
    extra_context = {
        "form_title": "Leave Request | Create",
        "form_submit": "Submit",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lt_list"] = LeaveType.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        obj = None
        form = self.form_class(request.POST)
        print("FOrm here")
        if not form.is_valid():
            print(form.data)
            return redirect("leavemanager:create")
        # saving the form
        obj = form.save(commit=False)
        print(f"leave_type - {obj.leave_type}")
        obj.employee = Employee.objects.get_or_none(user_id=request.user.id)
        if not obj.validate_leaves():
            obj.status = "rejected"
            obj.save()
        else:
            obj.status = "requested"
            obj.save()
            # obj.create_leaves()
        # obj.send_request()
        # obj.completed()
        return redirect("leavemanager:list")
