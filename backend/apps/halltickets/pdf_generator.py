import io
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings
from apps.scheduling.models import TimetableEntry
from apps.seating.models import SeatAssignment
from apps.students.models import SubjectRegistration, EligibilityStatus

def generate_hall_ticket_pdf(hall_ticket):
    """
    Generates an official Hall Ticket / Examination Pass PDF.
    Strictly follows the ExamForge Forest Green & Gold palette.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=portrait(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Color Palette (NO BLUE)
    c_forest = colors.HexColor('#14532D')
    c_emerald = colors.HexColor('#15803D')
    c_sage_light = colors.HexColor('#F4F9F4')
    c_gold = colors.HexColor('#D4A72C')
    c_charcoal = colors.HexColor('#242923')
    c_muted = colors.HexColor('#6B7280')
    c_border = colors.HexColor('#D1D5DB')

    inst_name = getattr(settings, 'EXAMFORGE_INSTITUTION_NAME', 'National Institute of Engineering & Technology')
    student = hall_ticket.student
    session = hall_ticket.session

    title_style = ParagraphStyle(
        'HTTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=c_forest,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'HTSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_emerald,
        alignment=1
    )

    cell_normal = ParagraphStyle(
        'CellNorm',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=c_charcoal
    )

    cell_bold = ParagraphStyle(
        'CellBld',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_charcoal
    )

    header_cell = ParagraphStyle(
        'HeaderC',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    # 1. Header
    story.append(Paragraph(inst_name.upper(), title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph(f"OFFICIAL EXAMINATION HALL TICKET / ADMIT CARD", subtitle_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(f"<font color='#6B7280' size='8.5'>{session.name} &nbsp;|&nbsp; Academic Year {session.academic_year}</font>", ParagraphStyle('HMeta', alignment=1)))
    story.append(Spacer(1, 12))

    # 2. Student Info Box
    info_data = [
        [
            Paragraph(f"<b>Ticket No:</b> {hall_ticket.ticket_number}", cell_normal),
            Paragraph(f"<b>Reg No:</b> <font color='#15803D'><b>{student.register_number}</b></font>", cell_normal),
            Paragraph(f"<b>Roll No:</b> {student.roll_number or 'N/A'}", cell_normal),
        ],
        [
            Paragraph(f"<b>Candidate Name:</b> {student.full_name.upper()}", cell_bold),
            Paragraph(f"<b>Branch:</b> {student.branch.name}", cell_normal),
            Paragraph(f"<b>Semester:</b> Sem {student.current_semester_number}", cell_normal),
        ],
        [
            Paragraph(f"<b>Department:</b> {student.branch.course.department.name}", cell_normal),
            Paragraph(f"<b>Status:</b> <font color='#16A34A'><b>VERIFIED & ELIGIBLE</b></font>", cell_normal),
            Paragraph(f"<b>Issued On:</b> {hall_ticket.issued_at.strftime('%d-%b-%Y')}", cell_normal),
        ]
    ]
    info_table = Table(info_data, colWidths=[180, 200, 160])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_sage_light),
        ('BOX', (0, 0), (-1, -1), 1, c_emerald),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 14))

    # 3. Schedule & Seating Table
    story.append(Paragraph("<b>REGISTERED EXAMINATIONS & ALLOCATED SEATING</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=10, textColor=c_forest)))
    story.append(Spacer(1, 4))

    registered_subjects = SubjectRegistration.objects.filter(
        student=student,
        eligibility_status=EligibilityStatus.ELIGIBLE
    ).values_list('subject_id', flat=True)

    entries = TimetableEntry.objects.filter(
        timetable__session=session,
        subject_config__subject_id__in=registered_subjects
    ).select_related('subject_config__subject', 'time_slot').order_by('exam_date', 'time_slot__start_time')

    if not entries.exists():
        # Fallback to general session entries for this branch
        entries = TimetableEntry.objects.filter(
            timetable__session=session,
            subject_config__subject__branch=student.branch,
            subject_config__subject__semester_number=student.current_semester_number
        ).select_related('subject_config__subject', 'time_slot').order_by('exam_date')

    sched_data = [
        [
            Paragraph("<b>Date & Shift</b>", header_cell),
            Paragraph("<b>Time</b>", header_cell),
            Paragraph("<b>Subject Code & Title</b>", header_cell),
            Paragraph("<b>Room & Seat</b>", header_cell),
            Paragraph("<b>Candidate Sign</b>", header_cell),
            Paragraph("<b>Invigilator Sign</b>", header_cell),
        ]
    ]

    for e in entries:
        # Check seat assignment
        seat = SeatAssignment.objects.filter(student=student, timetable_entry=e).first()
        room_seat_str = f"{seat.room_allocation.room.room_number} (Seat: {seat.seat_label})" if seat else "Assigned on Noticeboard"
        
        date_shift = f"{e.exam_date.strftime('%d-%b-%Y')}<br/><font color='#15803D' size='7.5'>{e.time_slot.get_shift_display()}</font>"
        time_str = f"{e.time_slot.start_time.strftime('%I:%M %p')} - {e.time_slot.end_time.strftime('%I:%M %p')}"
        subj_str = f"<b>{e.subject_config.subject.code}</b><br/>{e.subject_config.subject.name}"

        sched_data.append([
            Paragraph(date_shift, cell_normal),
            Paragraph(time_str, cell_normal),
            Paragraph(subj_str, cell_normal),
            Paragraph(room_seat_str, cell_bold),
            Paragraph("", cell_normal),
            Paragraph("", cell_normal),
        ])

    sched_table = Table(sched_data, colWidths=[90, 85, 175, 95, 45, 50])
    t_style = [
        ('BACKGROUND', (0, 0), (-1, 0), c_forest),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]
    for r in range(1, len(sched_data)):
        if r % 2 == 0:
            t_style.append(('BACKGROUND', (0, r), (-1, r), c_sage_light))
    sched_table.setStyle(TableStyle(t_style))
    story.append(sched_table)
    story.append(Spacer(1, 14))

    # 4. Examination Rules & Instructions
    rules_text = """
    <b>MANDATORY CANDIDATE INSTRUCTIONS:</b><br/>
    1. Candidates must report to the allocated examination hall at least <b>20 minutes before</b> the scheduled start time.<br/>
    2. Physical Hall Ticket and valid Institutional Identity Card are strictly mandatory for entry into the hall.<br/>
    3. Mobile phones, smartwatches, programmable calculators, notes, and electronic devices are strictly prohibited inside the hall.<br/>
    4. Candidates will not be permitted to leave the examination hall during the first 60 minutes or last 10 minutes of the session.<br/>
    5. Any form of malpractice or possession of unauthorized material will lead to immediate cancellation and disciplinary action.
    """
    story.append(Paragraph(rules_text, ParagraphStyle('Rules', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=c_charcoal)))
    story.append(Spacer(1, 20))

    # 5. Signatures
    sig_data = [
        [
            Paragraph("____________________________<br/><b>Signature of Candidate</b>", ParagraphStyle('S1', fontSize=8, alignment=0)),
            Paragraph(f"<b>Verification Token:</b><br/><font size='7' color='#6B7280'>{hall_ticket.barcode_token}</font>", ParagraphStyle('S2', fontSize=8, alignment=1)),
            Paragraph("____________________________<br/><b>Controller of Examinations</b>", ParagraphStyle('S3', fontSize=8, alignment=2)),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[180, 180, 180])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(KeepTogether(sig_table))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
