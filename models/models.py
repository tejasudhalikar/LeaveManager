from datetime import datetime, date as dtdate
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import pandas as pd
from django.dispatch import receiver

from qux.models import CoreModel, default_null_blank


department_choices = (
    ("IT", "it"),
    ("HR", "hr"),
    ("OPERATIONS", "operations"),
    ("ANALYSIS", "analysis"),
)


class LeaveAccruement(CoreModel):
    rate = models.FloatField()
    unit = models.CharField(
        max_length=20, choices=(("MONTH", "month"), ("YEAR", "year"))
    )

    class meta:
        verbose_name = "Leave Accruement"
        verbose_name_plural = "Leave Accruements"

    def __str__(self):
        return f"{self.rate} - {self.unit}"


class LeaveType(CoreModel):
    name = models.CharField(max_length=30, unique=True)
    carry_forward_days = models.IntegerField(default=0)
    is_encashable = models.BooleanField(default=False)
    encash_offset_days = models.IntegerField(**default_null_blank)
    leaves_available = models.IntegerField()
    accruement = models.ForeignKey(
        LeaveAccruement, on_delete=models.DO_NOTHING, **default_null_blank
    )

    class meta:
        ordering = ["name"]
        verbose_name = "Leave Type"
        verbose_name_plural = "Leave Types"

    def __str__(self):
        return f"{self.name}"


class Employee(CoreModel):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="employees",
        **default_null_blank,
    )
    department = models.CharField(max_length=25, choices=department_choices)
    designation = models.CharField(max_length=100)
    reporting_manager = models.ForeignKey(
        "self",
        on_delete=models.DO_NOTHING,
        **default_null_blank,
    )
    doj = models.DateField()
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20, unique=True)
    email_id = models.EmailField(unique=True)

    class meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ["doj"]

    def __str__(self):
        return f"{self.name}"

    def get_available_leaves(self, leave_type: LeaveType) -> int:
        accrued_leaves = 0
        balance_leaves = leave_type.leaves_available
        consumed_leaves = LeaveRequest.get_consumed_leaves(self, leave_type)
        if leave_type.accruement:
            accrued_leaves += self.get_accrued_leaves(
                leave_type.accruement, leave_type.carry_forward_days
            )
        leaves_available = (accrued_leaves + balance_leaves) - consumed_leaves
        # leaves_available = accrued_leaves + balance_leaves
        return 0 if leaves_available < 0 else leaves_available

    def get_accrued_leaves(
        self, accruement: LeaveAccruement, carry_forward_days: int
    ) -> int:
        today = datetime.now()
        doj = self.doj
        if accruement.unit.lower() == "month":
            months = today.month - doj.month
            years = today.year - doj.year
            if months < 0:
                years -= 1
                months += 12
            accrued_leaves = (accruement.rate * months) + (years * carry_forward_days)
        elif accruement.unit.lower() == "year":
            years = today.year - doj.year
            accrued_leaves = accruement.rate * years

        return accrued_leaves


class Holiday(CoreModel):
    name = models.CharField(max_length=30)
    date = models.DateField()

    class meta:
        verbose_name = "holiday"
        verbose_name_plural = "holidays"

    def __str__(self):
        return f"{self.name} - {self.date}"

    @classmethod
    def get_holidays_between(cls, from_date: dtdate, to_date: dtdate) -> list:
        holiday_list = []
        holidays = cls.objects.filter(date__range=(from_date, to_date))
        for holiday in holidays:
            holiday_list.append(holiday.date)
        return holiday_list

class LeaveRequest(CoreModel):
    slug = models.CharField(max_length=16, unique=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, **default_null_blank
    )
    leave_type = models.ForeignKey(
        LeaveType, on_delete=models.DO_NOTHING, **default_null_blank
    )
    reason = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=(
            ("approved", "approved"),
            ("rejected", "rejected"),
            ("requested", "requested"),
        ),
    )

    class meta:
        ordering = ["~dtm_created"]
        verbose_name = "Leave Request"
        verbose_name_plural = "Leave Requests"

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type.name}"
    
    def get_holidays(self):
        week_mask = "Sat Sun"
        holidays = set(Holiday.get_holidays_between(self.from_date, self.to_date))
        weekends = set(pd.bdate_range(
            start=self.from_date,
            end=self.to_date,
            freq="C",
            weekmask=week_mask,
        ).to_list())
        holidays = holidays.union(weekends)
        print(list(holidays))
        return list(holidays)


    @classmethod
    def get_consumed_leaves(cls, employee: Employee, leave_type: LeaveType) -> int:
        consumed_leaves = 0
        year_start = datetime(year=datetime.now().year, month=1, day=1)
        requests = cls.objects.filter(employee=employee, leave_type=leave_type)
        for request in requests:
            consumed_leaves += Leave.objects.filter(
                request=request, date__gt=year_start
            ).count()
        return consumed_leaves

    def validate_leaves(self) -> bool:
        days = (self.to_date - self.from_date).days
        holidays = len(self.get_holidays())
        req_days = days - holidays
        print(f"available leaves - {self.employee.get_available_leaves(self.leave_type)}, req_days - {req_days}")
        if self.employee.get_available_leaves(self.leave_type) < req_days:
            return False
        return True
    
    def create_leaves(self):
        days = set(pd.date_range(self.from_date, self.to_date, freq="D").to_list())
        holidays = set(self.get_holidays())
        days = days - holidays
        for day in days:
            Leave.objects.create(request=self, date=day)


class Leave(CoreModel):
    request = models.ForeignKey(
        LeaveRequest, on_delete=models.CASCADE, **default_null_blank
    )
    date = models.DateField()

    class meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.request} - {self.date}"


class LeaveApproval(CoreModel):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, **default_null_blank
    )
    leave_type = models.ForeignKey(
        LeaveType, on_delete=models.DO_NOTHING, **default_null_blank
    )
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=(("APPROVED", "approved"), ("REJECTED", "rejected"))
    )

    class meta:
        ordering = ["from_date"]
        verbose_name = "Leave Request"
        verbose_name_plural = "Leave Requests"

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type.name}"


@receiver(post_save, sender=LeaveRequest, dispatch_uid="update_leaves")
def update_leaves(sender, instance, **kwargs):
    if instance.status == "approved":
        instance.create_leaves()
