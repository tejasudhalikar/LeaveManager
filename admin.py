from django.apps import apps
from django.contrib import admin

from .models.models import Employee, Holiday, LeaveType, LeaveRequest, LeaveAccruement


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "user",
        "department",
        "designation",
        "reporting_manager",
        "doj",
        "address",
        "contact_number",
        "email_id",
    )
    list_display = fields
    readonly_fields = ("id",)


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "carry_forward_days",
        "is_encashable",
        "encash_offset_days",
        "leaves_available",
        "accruement",
    )
    list_display = fields
    readonly_fields = ("id",)


# @admin.register(LeaveApproval)
# class LeaveApprovalAdmin(admin.ModelAdmin):
#     fields = (
#         "employee",
#         "leave_type",
#         "from_date",
#         "to_date",
#         "status",
#     )
#     list_display = fields
#     readonly_fields = ("id",)
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    fields = (
        "employee",
        "leave_type",
        "from_date",
        "to_date",
        "status",
    )
    list_display = fields
    readonly_fields = ("id",)


@admin.register(LeaveAccruement)
class LeaveAccruementAdmin(admin.ModelAdmin):
    fields = (
        "rate",
        "unit",
    )
    list_display = fields
    readonly_fields = ("id",)

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "date",
    )
    list_display = fields
    readonly_fields = ("id",)
