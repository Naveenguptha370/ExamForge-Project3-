import io
import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings

def generate_timetable_pdf(timetable, department_id=None, branch_id=None):
    """
    Generates a high-quality, printable PDF of the examination timetable.
    Strictly uses the ExamForge Forest Green & Charcoal design palette.
    Returns bytes of the generated PDF file.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Define color palette (strictly NO BLUE)
    c_forest = colors.HexColor('#14532D')
    c_emerald = colors.HexColor('#15803D')
    c_sage_light = colors.HexColor('#F4F9F4')
    c_gold = colors.HexColor('#D4A72C')
    c_charcoal = colors.HexColor('#242923')
    c_muted = colors.HexColor('#6B7280')
    c_border = colors.HexColor('#D1D5DB')

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_forest,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_emerald,
        alignment=1
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_muted,
        alignment=1
    )

    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=c_charcoal
    )

    cell_normal = ParagraphStyle(
        'CellNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=c_charcoal
    )

    header_cell = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.white,
        alignment=1
    )

    # 1. Header Section
    inst_name = getattr(settings, 'EXAMFORGE_INSTITUTION_NAME', 'National Institute of Engineering & Technology')
    session = timetable.session

    story.append(Paragraph(inst_name.upper(), title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"OFFICIAL EXAMINATION TIMETABLE — {session.name.upper()}", subtitle_style))
    story.append(Spacer(1, 3))
    
    meta_text = (
        f"<b>Academic Year:</b> {session.academic_year} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Session Code:</b> {session.code} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Version:</b> v{timetable.version} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Status:</b> {timetable.get_status_display()} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Published:</b> {timetable.published_at.strftime('%d-%b-%Y') if timetable.published_at else 'Official Draft'}"
    )
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 15))

    # 2. Entries Query
    entries_qs = timetable.entries.select_related(
        'subject_config__subject',
        'subject_config__subject__department',
        'subject_config__subject__branch',
        'time_slot'
    ).order_by('exam_date', 'time_slot__start_time', 'subject_config__subject__code')

    if department_id:
        entries_qs = entries_qs.filter(subject_config__subject__department_id=department_id)
    if branch_id:
        entries_qs = entries_qs.filter(subject_config__subject__branch_id=branch_id)

    entries = list(entries_qs)

    if not entries:
        story.append(Paragraph("No scheduled examination entries found for the selected criteria.", meta_style))
    else:
        # Table Header
        table_data = [
            [
                Paragraph("<b>Date & Day</b>", header_cell),
                Paragraph("<b>Time Slot & Shift</b>", header_cell),
                Paragraph("<b>Subject Code</b>", header_cell),
                Paragraph("<b>Subject Title</b>", header_cell),
                Paragraph("<b>Department / Branch</b>", header_cell),
                Paragraph("<b>Sem</b>", header_cell),
                Paragraph("<b>Credits</b>", header_cell),
                Paragraph("<b>QP Code</b>", header_cell)
            ]
        ]

        for idx, entry in enumerate(entries):
            subj = entry.subject_config.subject
            day_name = entry.exam_date.strftime('%A')
            date_str = f"{entry.exam_date.strftime('%d-%b-%Y')}<br/><font color='#6B7280' size='7.5'>{day_name}</font>"
            slot_str = f"{entry.time_slot.start_time.strftime('%I:%M %p')} - {entry.time_slot.end_time.strftime('%I:%M %p')}<br/><font color='#15803D' size='7.5'>{entry.time_slot.get_shift_display()}</font>"
            
            dept_branch = subj.branch.name if subj.branch else (subj.department.name if subj.department else "Common Core")
            qp_code = entry.subject_config.question_paper_code or f"QP-{subj.code}"

            table_data.append([
                Paragraph(date_str, cell_bold),
                Paragraph(slot_str, cell_normal),
                Paragraph(f"<b>{subj.code}</b>", cell_bold),
                Paragraph(f"<b>{subj.name}</b>", cell_normal),
                Paragraph(dept_branch, cell_normal),
                Paragraph(str(subj.semester_number), cell_normal),
                Paragraph(str(subj.credits), cell_normal),
                Paragraph(f"<font color='#6B7280'>{qp_code}</font>", cell_normal),
            ])

        # Widths for landscape letter (total width ~ 720pt)
        col_widths = [85, 110, 75, 190, 140, 35, 40, 65]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        t_style = [
            ('BACKGROUND', (0, 0), (-1, 0), c_forest),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]

        # Alternating row colors
        for r in range(1, len(table_data)):
            bg = c_sage_light if r % 2 == 0 else colors.white
            t_style.append(('BACKGROUND', (0, r), (-1, r), bg))

        table.setStyle(TableStyle(t_style))
        story.append(table)

    # 3. Footer / Signature Section
    story.append(Spacer(1, 30))
    sig_data = [
        [
            Paragraph("<b>Prepared & Verified by:</b><br/><br/><br/>___________________________<br/><b>Assistant Controller of Exams</b>", cell_normal),
            Paragraph("<b>Endorsed by:</b><br/><br/><br/>___________________________<br/><b>Dean (Academic Affairs)</b>", cell_normal),
            Paragraph("<b>Approved & Issued by:</b><br/><br/><br/>___________________________<br/><b>Controller of Examinations</b><br/><i>(Office of the Registrar)</i>", cell_normal),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[240, 240, 240])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(KeepTogether(sig_table))

    # Build document
    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data
