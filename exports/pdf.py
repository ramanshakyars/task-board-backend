from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def export_tasks_to_pdf(queryset) -> BytesIO:
   
    ouput = BytesIO()
    doc = SimpleDocTemplate(
        ouput,
        pagesize=landscape(letter),
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )

    styes = getSampleStyleSheet()
    elemnts = []

    # Titl
    elemnts.append(Paragraph("Task Board — Task List", styes["Title"]))
    elemnts.append(Spacer(1, 0.2 * inch))

    # Tabel header
    headers = ["ID", "Code", "Name", "Priority", "Status", "Due Date", "Created By"]
    tabel_data = [headers]

    for task in queryset:
        tabel_data.append([
            str(task.id),
            task.code,
            task.name[:40] + "..." if len(task.name) > 40 else task.name,
            task.get_priority_display(),
            task.get_status_display(),
            str(task.due_date) if task.due_date else "—",
            task.created_by.username if task.created_by else "—",
        ])

    tabel = Table(tabel_data, repeatRows=1)
    tabel.setStyle(TableStyle([
        # Headr styling
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2D6A4F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        # Data ros
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0F4F0")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elemnts.append(tabel)

    doc.build(elemnts)
    ouput.seek(0)
    return ouput
