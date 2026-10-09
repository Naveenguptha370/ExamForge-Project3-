from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from infrastructure.models import Room, RoomMaintenance, RoomAssignment
from seating.models import SeatingPlan, SeatAllocation
from invigilation.models import InvigilatorDuty, DutyRequirement
from academics.models import Faculty, Student
from examinations.models import Examination, ExamSession


class OperationsDashboardView(APIView):
    """
    Consolidated real-time operations dashboard for Room Infrastructure,
    Seating Arrangement, and Invigilator Allocation.
    All figures are calculated directly from live database tables.
    """

    def get(self, request):
        # 1. Room metrics
        rooms = Room.objects.filter(is_active=True)
        total_rooms = rooms.count()
        total_physical_capacity = rooms.aggregate(Sum('capacity'))['capacity__sum'] or 0
        total_usable_capacity = rooms.aggregate(Sum('usable_capacity'))['usable_capacity__sum'] or 0

        # Maintenance rooms
        maintenance_rooms = RoomMaintenance.objects.filter(is_resolved=False).values_list('room_id', flat=True)
        maintenance_count = len(set(maintenance_rooms))

        # Occupied rooms (active assignments)
        occupied_rooms = RoomAssignment.objects.filter(status__in=['reserved', 'active']).values_list('room_id', flat=True)
        occupied_count = len(set(occupied_rooms))

        available_rooms_count = max(0, total_rooms - occupied_count - maintenance_count)

        # 2. Seating & Student metrics
        total_students = Student.objects.filter(is_eligible_for_exam=True).count()
        total_seat_allocations = SeatAllocation.objects.count()
        
        # Pending seating exams
        examinations = Examination.objects.all()
        total_exams = examinations.count()
        exams_with_seating = SeatingPlan.objects.filter(status__in=['validated', 'approved']).count()
        seating_completion_rate = round((exams_with_seating / total_exams * 100), 1) if total_exams > 0 else 0

        # Unallocated students in draft/shortage seating plans
        plans_with_shortage = SeatingPlan.objects.filter(capacity_shortage__gt=0)
        total_unallocated_students = sum(p.capacity_shortage for p in plans_with_shortage)

        # 3. Invigilator metrics
        total_faculty = Faculty.objects.filter(is_active=True).count()
        total_duties_assigned = InvigilatorDuty.objects.count()

        # Unstaffed room calculation:
        # Check examinations that have room assignments but shortage of invigilators
        unstaffed_alerts = []
        for exam in examinations.filter(status__in=['seating_generated', 'invigilators_assigned']):
            for ra in exam.room_assignments.all():
                duties_in_room = exam.invigilator_duties.filter(room=ra.room).count()
                req = exam.invigilation_requirements.filter(room=ra.room).first()
                needed = req.required_invigilators if req else (2 if ra.allotted_students_count > 30 else 1)
                if duties_in_room < needed:
                    shortage = needed - duties_in_room
                    unstaffed_alerts.append({
                        'exam_id': exam.id,
                        'subject_code': exam.subject.code,
                        'exam_date': str(exam.exam_date),
                        'time_slot': exam.time_slot.name,
                        'room_number': ra.room.room_number,
                        'building_name': ra.room.building.name,
                        'needed': needed,
                        'assigned': duties_in_room,
                        'shortage': shortage,
                        'severity': 'high' if duties_in_room == 0 else 'medium'
                    })

        # Conflict count
        # E.g. overlapping duties or rooms under maintenance assigned to exams
        room_conflicts = 0
        for m in RoomMaintenance.objects.filter(is_resolved=False):
            conflicting_ra = RoomAssignment.objects.filter(
                room=m.room,
                examination__exam_date__gte=m.start_date,
                examination__exam_date__lte=m.end_date
            ).count()
            room_conflicts += conflicting_ra

        return Response({
            'infrastructure': {
                'total_rooms': total_rooms,
                'available_rooms': available_rooms_count,
                'occupied_rooms': occupied_count,
                'maintenance_rooms': maintenance_count,
                'total_physical_capacity': total_physical_capacity,
                'total_usable_capacity': total_usable_capacity,
                'room_conflicts': room_conflicts,
            },
            'seating': {
                'total_students': total_students,
                'total_allocated': total_seat_allocations,
                'students_awaiting_allocation': total_unallocated_students,
                'seating_completion_rate': seating_completion_rate,
                'total_exams': total_exams,
                'exams_with_seating': exams_with_seating,
            },
            'invigilation': {
                'total_faculty': total_faculty,
                'total_duties_assigned': total_duties_assigned,
                'unstaffed_rooms_count': len(unstaffed_alerts),
                'unstaffed_alerts': unstaffed_alerts,
                'average_workload': round((total_duties_assigned / total_faculty), 1) if total_faculty > 0 else 0,
            }
        })
