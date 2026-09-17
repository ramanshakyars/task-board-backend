from io import BytesIO

from django.db import transaction
from django.http import HttpResponse

from exports.excel import export_tasks_to_excel
from exports.pdf import export_tasks_to_pdf

from .models import Task


def reorder_tasks(ordered_ids: list) -> None:
  
    with transaction.atomic():
        for index, task_id in enumerate(ordered_ids):
            Task.objects.filter(pk=task_id).update(order=index)


def get_excel_response(queryset) -> HttpResponse:
    ouput: BytesIO = export_tasks_to_excel(queryset)
    responce = HttpResponse(
        ouput.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    responce["Content-Disposition"] = 'attachment; filename="tasks.xlsx"'
    return responce


def get_pdf_response(queryset) -> HttpResponse:
    ouput: BytesIO = export_tasks_to_pdf(queryset)
    responce = HttpResponse(ouput.getvalue(), content_type="application/pdf")
    responce["Content-Disposition"] = 'attachment; filename="tasks.pdf"'
    return responce
