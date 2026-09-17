from django.urls import re_path
from .views import (
    TaskDetailView,
    TaskExportExcelView,
    TaskExportPDFView,
    TaskListCreateView,
    TaskReorderView,
)

urlpatterns = [
    re_path(r"^/?$", TaskListCreateView.as_view(), name="task-list-create"),
    re_path(r"^/?reorder/?$", TaskReorderView.as_view(), name="task-reorder"),
    re_path(r"^/?export/excel/?$", TaskExportExcelView.as_view(), name="task-export-excel"),
    re_path(r"^/?export/pdf/?$", TaskExportPDFView.as_view(), name="task-export-pdf"),
    re_path(r"^/?(?P<pk>\d+)/?$", TaskDetailView.as_view(), name="task-detail"),
]
