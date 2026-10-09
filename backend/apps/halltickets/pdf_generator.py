import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.conf import settings

def generate_hall_ticket_pdf(hall_ticket):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Brand Colors (Zero Blue - Forest Green Palette)
    forest_green = colors.HexColor('#14532D')
    emerald_green = colors.HexColor('#15803D')
    sage_green = colors.HexColor('#DDEBDD')
    gold_accent = colors.HexColor('#D4A72C')
    charcoal = colors.HexColor('#242923')
    light_border = colors.HexColor('#E7E5E4')

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=forest_green,
        alignment=1  # Centered
    )

    sub_title_style = ParagraphStyle(
        'SubTitle',
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=emerald_green,
        alignment=1
    )

    badge_style = ParagraphStyle(
        'DocBadge',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.white,
        alignment=1
    )

    label_style = ParagraphStyle(
        'FieldLabel',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=forest_green
    )

    val_style = ParagraphStyle(
        'FieldValue',
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        textColor=charcoal
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    rules_style = ParagraphStyle(
        'RulesText',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=charcoal
    )

    # 1. Header Banner
    story.append(Paragraph("EXAMFORGE UNIVERSITY", title_style))
    story.append(Paragraph("OFFICE OF THE CONTROLLER OF EXAMINATIONS", sub_title_style))
    story.append(Spacer(1, 8))

    # Badge Bar
    badge_data = [[Paragraph(f"OFFICIAL HALL TICKET / ADMIT CARD — {hall_ticket.exam_session.name.upper()}", badge_style)]]
    badge_table = Table(badge_data, colWidths=[520])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), forest_green),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 12))

    # 2. Student Information Table
    student = hall_ticket.student
    student_info_data = [
        [
            Paragraph("Student Name:", label_style),
            Paragraph(student.full_name, val_style),
            Paragraph("Hall Ticket No:", label_style),
            Paragraph(hall_ticket.ticket_number, val_style)
        ],
        [
            Paragraph("Roll Number:", label_style),
            Paragraph(student.roll_no, val_style),
            Paragraph("Registration No:", label_style),
            Paragraph(student.registration_no, val_style)
        ],
        [
            Paragraph("Department:", label_style),
            Paragraph(student.department.name, val_style),
            Paragraph("Academic Year:", label_style),
            Paragraph(hall_ticket.exam_session.academic_year, val_style)
        ],
        [
            Paragraph("Course / Branch:", label_style),
            Paragraph(f"{student.course.code} - {student.branch.code if student.branch else 'General'}", val_style),
            Paragraph("Semester:", label_style),
            Paragraph(f"Semester {student.semester.number}", val_style)
        ]
    ]

    student_table = Table(student_info_data, colWidths=[100, 160, 100, 160])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FBFBF9')),
        ('BOX', (0, 0), (-1, -1), 1, light_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, light_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(student_table)
    story.append(Spacer(1, 14))

    # 3. Scheduled Examinations Table
    exam_schedule_headers = [
        Paragraph("Date", table_header_style),
        Paragraph("Time / Slot", table_header_style),
        Paragraph("Subject Code", table_header_style),
        Paragraph("Subject Name", table_header_style),
        Paragraph("Room", table_header_style),
        Paragraph("Seat No", table_header_style),
    ]

    exam_rows = [exam_schedule_headers]
    entries = list(hall_ticket.entries.all())

    if not entries:
        exam_rows.append([
            Paragraph("Schedule pending", val_style),
            Paragraph("-", val_style),
            Paragraph("-", val_style),
            Paragraph("Examination schedule will be updated upon final timetable publication", val_style),
            Paragraph("-", val_style),
            Paragraph("-", val_style),
        ])
    else:
        for ent in entries:
            exam_rows.append([
                Paragraph(ent.exam_date.strftime('%d-%b-%Y'), val_style),
                Paragraph(ent.time_slot_str, val_style),
                Paragraph(ent.exam_subject.subject.code, val_style),
                Paragraph(ent.exam_subject.subject.name, val_style),
                Paragraph(ent.room_number, val_style),
                Paragraph(ent.seat_label, val_style),
            ])

    schedule_table = Table(exam_rows, colWidths=[65, 95, 65, 175, 60, 60])
    schedule_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), emerald_green),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, light_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, light_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, sage_green]),
    ]))
    story.append(schedule_table)
    story.append(Spacer(1, 14))

    # 4. Mandatory Examination Rules & Instructions
    story.append(Paragraph("IMPORTANT CANDIDATE INSTRUCTIONS", label_style))
    story.append(Spacer(1, 4))

    instructions = [
        "1. Candidates must produce this verified Hall Ticket along with valid Institution ID card in every examination session.",
        "2. Candidates must report to their assigned Examination Hall at least 20 minutes prior to the commencement of the exam.",
        "3. Mobile phones, smart watches, programmable calculators, notes, or digital memory devices are strictly banned.",
        "4. Any candidate engaging in unauthorized communication or possessing unpermitted materials will be charged under Malpractice Regulations.",
        "5. Candidates will not be permitted to leave the examination hall during the first 60 minutes or last 10 minutes of the session."
    ]

    for inst in instructions:
        story.append(Paragraph(inst, rules_style))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 18))

    # 5. Verification Code & Signatures Footer
    footer_data = [
        [
            Paragraph(f"<b>Verification Security Hash:</b><br/>{str(hall_ticket.verification_hash)[:24]}...", rules_style),
            Paragraph("<b>Candidate's Signature:</b><br/><br/>______________________", rules_style),
            Paragraph("<b>Controller of Examinations:</b><br/><br/>[Digitally Approved]", rules_style),
        ]
    ]

    footer_table = Table(footer_data, colWidths=[200, 160, 160])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(footer_table)

    # Build Document
    doc.build(story)
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value
