import io
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils import timezone
from django.db import transaction
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from .models import ExamAttendanceSheet, AttendanceRecord, AttendanceCorrectionAudit
from .serializers import ExamAttendanceSheetSerializer, AttendanceRecordSerializer
from apps.seating.models import SeatingPlan, SeatAllocation
from apps.examinations.models import ExamSubject
from apps.infrastructure.models import ExaminationRoom

class ExamAttendanceSheetViewSet(viewsets.ModelViewSet):
    queryset = ExamAttendanceSheet.objects.select_related('exam_subject__subject', 'room__building', 'invigilator__user').prefetch_related('records__student').all()
    serializer_class = ExamAttendanceSheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        exam_subject_id = self.request.query_params.get('exam_subject')
        room_id = self.request.query_params.get('room')
        date = self.request.query_params.get('date')
        if exam_subject_id:
            qs = qs.filter(exam_subject_id=exam_subject_id)
        if room_id:
            qs = qs.filter(room_id=room_id)
        if date:
            qs = qs.filter(exam_subject__planned_date=date)
        return qs

    @action(detail=False, methods=['post'])
    def init_from_seating(self, request):
        exam_subject_id = request.data.get('exam_subject_id')
        room_id = request.data.get('room_id')

        if not exam_subject_id or not room_id:
            return Response({'error': 'exam_subject_id and room_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        plan = SeatingPlan.objects.filter(exam_subject_id=exam_subject_id, room_id=room_id).first()
        if not plan:
            return Response({'error': 'No seating plan found for this subject and room. Generate seating first.'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            sheet, _ = ExamAttendanceSheet.objects.get_or_create(
                exam_subject_id=exam_subject_id,
                room_id=room_id,
                defaults={'recorded_by': request.user}
            )

            allocations = SeatAllocation.objects.filter(seating_plan=plan).select_related('student', 'seat')
            for alloc in allocations:
                AttendanceRecord.objects.get_or_create(
                    sheet=sheet,
                    student=alloc.student,
                    defaults={'seat_label': alloc.seat.seat_label, 'status': AttendanceRecord.Status.PRESENT}
                )

            # Update counts
            total = sheet.records.count()
            present = sheet.records.filter(status='PRESENT').count()
            sheet.total_students = total
            sheet.present_count = present
            sheet.absent_count = sheet.records.filter(status='ABSENT').count()
            sheet.malpractice_count = sheet.records.filter(status='MALPRACTICE').count()
            sheet.save()

        return Response({
            'message': f'Attendance sheet initialized with {total} candidates.',
            'sheet': ExamAttendanceSheetSerializer(sheet).data
        })

    @action(detail=True, methods=['post'])
    def mark_batch(self, request, pk=None):
        sheet = self.get_object()
        records_data = request.data.get('records', [])

        with transaction.atomic():
            for item in records_data:
                record_id = item.get('id')
                new_status = item.get('status', 'PRESENT')
                booklet_no = item.get('answer_booklet_no', '')
                remarks = item.get('remarks', '')

                rec = AttendanceRecord.objects.filter(id=record_id, sheet=sheet).first()
                if rec:
                    if rec.status != new_status:
                        AttendanceCorrectionAudit.objects.create(
                            attendance_record=rec,
                            previous_status=rec.status,
                            new_status=new_status,
                            reason=item.get('reason', 'Bulk attendance update during exam'),
                            corrected_by=request.user
                        )
                    rec.status = new_status
                    rec.answer_booklet_no = booklet_no
                    rec.remarks = remarks
                    rec.updated_by = request.user
                    rec.save()

            # Recalculate summary metrics
            records = sheet.records.all()
            sheet.total_students = records.count()
            sheet.present_count = records.filter(status='PRESENT').count()
            sheet.absent_count = records.filter(status='ABSENT').count()
            sheet.malpractice_count = records.filter(status='MALPRACTICE').count()
            sheet.is_submitted = True
            sheet.submitted_at = timezone.now()
            sheet.recorded_by = request.user
            sheet.save()

        return Response({
            'message': 'Attendance successfully recorded and submitted.',
            'sheet': ExamAttendanceSheetSerializer(sheet).data
        })

    @action(detail=True, methods=['get'])
    def printable_sheet(self, request, pk=None):
        sheet = self.get_object()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
        story = []
        styles = getSampleStyleSheet()

        forest_green = colors.HexColor('#14532D')
        emerald_green = colors.HexColor('#15803D')
        light_border = colors.HexColor('#E7E5E4')

        title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=forest_green, alignment=1)
        sub_style = ParagraphStyle('Sub', fontName='Helvetica', fontSize=10, leading=13, textColor=colors.HexColor('#242923'), alignment=1)
        th_style = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=1)
        cell_style = ParagraphStyle('Cell', fontName='Helvetica', fontSize=8, leading=10, textColor=colors.HexColor('#242923'))

        story.append(Paragraph("EXAMFORGE — OFFICIAL EXAMINATION ATTENDANCE SHEET", title_style))
        story.append(Paragraph(f"Subject: {sheet.exam_subject.subject.code} - {sheet.exam_subject.subject.name} | Room: {sheet.room.room_number}", sub_style))
        date_str = sheet.exam_subject.planned_date.strftime('%d-%b-%Y') if sheet.exam_subject.planned_date else 'TBD'
        slot_str = sheet.exam_subject.time_slot.name if sheet.exam_subject.time_slot else 'Morning'
        story.append(Paragraph(f"Date: {date_str} | Slot: {slot_str} | Total Candidates: {sheet.total_students}", sub_style))
        story.append(Spacer(1, 10))

        headers = [
            Paragraph("S.No", th_style),
            Paragraph("Seat", th_style),
            Paragraph("Roll Number", th_style),
            Paragraph("Student Name", th_style),
            Paragraph("Booklet No", th_style),
            Paragraph("Status", th_style),
            Paragraph("Candidate Signature", th_style),
        ]
        table_rows = [headers]

        for idx, rec in enumerate(sheet.records.all(), start=1):
            table_rows.append([
                Paragraph(str(idx), cell_style),
                Paragraph(rec.seat_label, cell_style),
                Paragraph(rec.student.roll_no, cell_style),
                Paragraph(rec.student.full_name, cell_style),
                Paragraph(rec.answer_booklet_no or "___________", cell_style),
                Paragraph(rec.get_status_display(), cell_style),
                Paragraph("__________________", cell_style),
            ])

        t = Table(table_rows, colWidths=[30, 45, 80, 140, 85, 60, 80])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), forest_green),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, light_border),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))

        story.append(Paragraph("<b>Invigilator Signature:</b> ___________________________    <b>Chief Superintendent:</b> ___________________________", sub_style))

        doc.build(story)
        pdf_val = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf_val, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Attendance_{sheet.room.room_number}.pdf"'
        return response


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related('sheet', 'student').prefetch_related('correction_audits').all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def correct_status(self, request, pk=None):
        rec = self.get_object()
        new_status = request.data.get('status')
        reason = request.data.get('reason')

        if not new_status or not reason:
            return Response({'error': 'status and reason are required for correction audit'}, status=status.HTTP_400_BAD_REQUEST)

        prev = rec.status
        rec.status = new_status
        rec.updated_by = request.user
        rec.save()

        AttendanceCorrectionAudit.objects.create(
            attendance_record=rec,
            previous_status=prev,
            new_status=new_status,
            reason=reason,
            corrected_by=request.user
        )

        # Update sheet counts
        sheet = rec.sheet
        sheet.present_count = sheet.records.filter(status='PRESENT').count()
        sheet.absent_count = sheet.records.filter(status='ABSENT').count()
        sheet.malpractice_count = sheet.records.filter(status='MALPRACTICE').count()
        sheet.save()

        return Response({'message': f'Attendance updated from {prev} to {new_status} with audit log recorded.'})
