from django.urls import path

from ..views.appviews import (
    LeaveRequestListView,
    LeaveRequestCreateView,
    LeaveRequestApproveView,
)

app_name = "leavemanager"

urlpatterns = [
    path("", LeaveRequestListView.as_view(), name="list"),
    path("create/", LeaveRequestCreateView.as_view(), name="create"),
    # path("delete/<str:slug>", LeaveRequestDeleteView.as_view(), name="delete"),
    path("approve/<str:slug>", LeaveRequestApproveView.as_view(), name="approve"),
]
