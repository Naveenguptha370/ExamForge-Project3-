from rest_framework import serializers
from .models import SeatingPlan, Seat, SeatAllocation
from infrastructure.serializers import RoomSerializer


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'room', 'row_index', 'col_index', 'seat_label', 'is_usable']


class SeatAllocationSerializer(serializers.ModelSerializer):
    student_roll_no = serializers.CharField(source='student.roll_no', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_dept_code = serializers.CharField(source='student.department.code', read_only=True)
    student_course_code = serializers.CharField(source='student.course.code', read_only=True)
    student_reg_no = serializers.CharField(source='student.registration_no', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='room.building.name', read_only=True)
    row_index = serializers.IntegerField(source='seat.row_index', read_only=True)
    col_index = serializers.IntegerField(source='seat.col_index', read_only=True)

    class Meta:
        model = SeatAllocation
        fields = [
            'id', 'seating_plan', 'examination', 'student', 'student_roll_no',
            'student_name', 'student_dept_code', 'student_course_code', 'student_reg_no',
            'room', 'room_number', 'building_name', 'seat', 'seat_label',
            'row_index', 'col_index', 'allocation_type', 'allocated_at'
        ]


class SeatingPlanSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='examination.subject.code', read_only=True)
    subject_name = serializers.CharField(source='examination.subject.name', read_only=True)
    exam_date = serializers.DateField(source='examination.exam_date', read_only=True)
    time_slot_name = serializers.CharField(source='examination.time_slot.name', read_only=True)
    spacing_rule_display = serializers.CharField(source='get_spacing_rule_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    assigned_rooms = serializers.SerializerMethodField()

    class Meta:
        model = SeatingPlan
        fields = [
            'id', 'examination', 'subject_code', 'subject_name', 'exam_date',
            'time_slot_name', 'session_title', 'spacing_rule', 'spacing_rule_display',
            'status', 'status_display', 'total_allocated', 'total_unallocated',
            'capacity_shortage', 'validation_status', 'validation_notes',
            'assigned_rooms', 'created_at', 'updated_at'
        ]

    def get_assigned_rooms(self, obj):
        assignments = obj.examination.room_assignments.select_related('room', 'room__building')
        return [
            {
                'room_id': a.room.id,
                'room_number': a.room.room_number,
                'building_name': a.room.building.name,
                'usable_capacity': a.room.usable_capacity,
                'allotted_students_count': a.allotted_students_count
            }
            for a in assignments
        ]
