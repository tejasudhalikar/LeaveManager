from django.forms import ModelForm
from ..models.models import LeaveRequest


class LeaveRequestForm(ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ("leave_type", "reason", "from_date", "to_date")
