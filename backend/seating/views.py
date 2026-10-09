from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import SeatingPlan, Seat, SeatAllocation
from .serializers import SeatingPlanSerializer, SeatAllocationSerializer, SeatSerializer
from .engine import SeatingEngine
from infrastructure.models import Room, RoomAssignment
from examinations.models import Examination


class SeatingPlanViewSet(viewsets.ModelViewSet):
    queryset = SeatingPlan.objects.all().select_related('examination', 'examination__subject', 'examination__session', 'examination__time_slot')
    serializer_class = SeatingPlanSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        exam_id = self.request.query_params.get('examination')
        if exam_id:
            qs = qs.filter(examination_id=exam_id)
        return qs

    @action(detail=False, methods=['post'])
    def generate(self, request):
        exam_id = request.data.get('examination_id')
        room_ids = request.data.get('room_ids', [])
        spacing_rule = request.data.get('spacing_rule', 'department_separated')

        if not exam_id:
            return Response({'error': 'examination_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = SeatingEngine.generate(int(exam_id), [int(r) for r in room_ids], spacing_rule)
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e.message if hasattr(e, 'message') else e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def revalidate(self, request, pk=None):
        plan = self.get_object()
        result = SeatingEngine.revalidate(plan.examination_id)
        return Response(result)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        plan = self.get_object()
        if plan.capacity_shortage > 0:
            return Response(
                {'error': f"Cannot approve plan with unresolved capacity shortage ({plan.capacity_shortage} students unallocated)."},
                status=status.HTTP_400_BAD_REQUEST
            )
        plan.status = 'approved'
        plan.save()
        return Response({'status': 'approved', 'message': 'Seating plan approved for printing and publication.'})

    @action(detail=False, methods=['get'])
    def room_layout(self, request):
        """
        Returns the visual grid layout of a specific room for a specific examination.
        Contains grid dimensions, all seats, and which students are seated where.
        """
        exam_id = request.query_params.get('examination_id')
        room_id = request.query_params.get('room_id')

        if not exam_id or not room_id:
            return Response({'error': 'Both examination_id and room_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exam_id_int = int(exam_id)
            room_id_int = int(room_id)
        except (ValueError, TypeError):
            return Response({'error': 'examination_id and room_id must be valid numbers'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exam = Examination.objects.select_related('subject', 'time_slot').get(id=exam_id_int)
            room = Room.objects.select_related('building').get(id=room_id_int)
        except (Examination.DoesNotExist, Room.DoesNotExist):
            return Response({'error': 'Examination or Room not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all seats in this room
        seats = Seat.objects.filter(room=room).order_by('row_index', 'col_index')
        # Fetch all allocations in this room for this exam
        allocations = SeatAllocation.objects.filter(
            examination=exam,
            room=room
        ).select_related('student', 'student__department', 'student__course', 'seat')

        alloc_map = {a.seat_id: a for a in allocations}

        grid = []
        for s in seats:
            alloc = alloc_map.get(s.id)
            seat_data = {
                'seat_id': s.id,
                'row_index': s.row_index,
                'col_index': s.col_index,
                'seat_label': s.seat_label,
                'is_usable': s.is_usable,
                'is_occupied': alloc is not None,
                'student': {
                    'allocation_id': alloc.id,
                    'roll_no': alloc.student.roll_no,
                    'name': alloc.student.name,
                    'department': alloc.student.department.code,
                    'course': alloc.student.course.code,
                    'registration_no': alloc.student.registration_no,
                    'allocation_type': alloc.allocation_type
                } if alloc else None
            }
            grid.append(seat_data)

        # Check invigilator duty for this room
        duties = exam.invigilator_duties.filter(room=room).select_related('faculty', 'faculty__department')
        invigilators = [
            {
                'id': d.id,
                'name': d.faculty.name,
                'employee_id': d.faculty.employee_id,
                'department': d.faculty.department.code,
                'role': d.get_role_display(),
                'status': d.status
            }
            for d in duties
        ]

        return Response({
            'examination': {
                'id': exam.id,
                'subject_code': exam.subject.code,
                'subject_name': exam.subject.name,
                'exam_date': exam.exam_date,
                'time_slot': exam.time_slot.name
            },
            'room': {
                'id': room.id,
                'room_number': room.room_number,
                'building_name': room.building.name,
                'rows': room.rows,
                'columns': room.columns,
                'capacity': room.capacity,
                'usable_capacity': room.usable_capacity,
                'total_allocated': len(allocations),
            },
            'invigilators': invigilators,
            'grid': grid
        })

    @action(detail=False, methods=['post'])
    def swap_seat(self, request):
        allocation_id = request.data.get('allocation_id')
        target_room_id = request.data.get('target_room_id')
        target_seat_id = request.data.get('target_seat_id')

        if not all([allocation_id, target_room_id, target_seat_id]):
            return Response({'error': 'allocation_id, target_room_id, and target_seat_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = SeatingEngine.swap_or_move(int(allocation_id), int(target_room_id), int(target_seat_id))
            return Response(result)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def printable_attendance(self, request):
        """
        Returns structured room-wise attendance sheet with student roll numbers,
        names, seat numbers, subject, invigilator details, and signature placeholders.
        """
        exam_id = request.query_params.get('examination_id')
        room_id = request.query_params.get('room_id')

        if not exam_id or not room_id:
            return Response({'error': 'Both examination_id and room_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exam_id_int = int(exam_id)
            room_id_int = int(room_id)
        except (ValueError, TypeError):
            return Response({'error': 'examination_id and room_id must be valid numbers'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exam = Examination.objects.select_related('subject', 'session', 'time_slot').get(id=exam_id_int)
            room = Room.objects.select_related('building').get(id=room_id_int)
        except (Examination.DoesNotExist, Room.DoesNotExist):
            return Response({'error': 'Examination or Room not found'}, status=status.HTTP_404_NOT_FOUND)

        allocations = SeatAllocation.objects.filter(
            examination=exam,
            room=room
        ).select_related('student', 'student__department', 'seat').order_by('seat__row_index', 'seat__col_index')

        duties = exam.invigilator_duties.filter(room=room).select_related('faculty')

        students_data = [
            {
                'sno': idx + 1,
                'seat_label': a.seat_label,
                'roll_no': a.student.roll_no,
                'name': a.student.name,
                'department': a.student.department.code,
                'reg_no': a.student.registration_no,
            }
            for idx, a in enumerate(allocations)
        ]

        return Response({
            'session_name': exam.session.name,
            'academic_year': exam.session.academic_year,
            'subject_code': exam.subject.code,
            'subject_name': exam.subject.name,
            'exam_date': exam.exam_date,
            'time_slot': exam.time_slot.name,
            'room_number': room.room_number,
            'building_name': room.building.name,
            'floor': room.floor,
            'total_students': len(students_data),
            'invigilators': [d.faculty.name for d in duties],
            'students': students_data
        })


class SeatAllocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SeatAllocation.objects.all().select_related(
        'examination', 'student', 'room', 'seat', 'student__department', 'student__course', 'room__building'
    )
    serializer_class = SeatAllocationSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        exam_id = self.request.query_params.get('examination')
        room_id = self.request.query_params.get('room')
        student_id = self.request.query_params.get('student')
        if exam_id:
            qs = qs.filter(examination_id=exam_id)
        if room_id:
            qs = qs.filter(room_id=room_id)
        if student_id:
            qs = qs.filter(student_id=student_id)
        return qs
