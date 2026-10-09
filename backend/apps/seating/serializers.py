from rest_framework import serializers
from .models import SeatingPlan, RoomAllocation, SeatAssignment

class SeatAssignmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    register_number = serializers.CharField(source='student.register_number', read_only=True)
    branch_name = serializers.CharField(source='student.branch.name', read_only=True)
    subject_code = serializers.CharField(source='timetable_entry.subject_config.subject.code', read_only=True)
    subject_name = serializers.CharField(source='timetable_entry.subject_config.subject.name', read_only=True)

    class Meta:
        model = SeatAssignment
        fields = '__all__'


class RoomAllocationSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    block_code = serializers.CharField(source='room.block.code', read_only=True)
    block_name = serializers.CharField(source='room.block.name', read_only=True)
    invigilator_name = serializers.CharField(source='primary_invigilator.full_name', read_only=True, allow_null=True)
    seat_assignments = SeatAssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = RoomAllocation
        fields = '__all__'


class SeatingPlanSerializer(serializers.ModelSerializer):
    time_slot_name = serializers.CharField(source='time_slot.name', read_only=True)
    session_code = serializers.CharField(source='session.code', read_only=True)
    room_allocations = RoomAllocationSerializer(many=True, read_only=True)

    class Meta:
        model = SeatingPlan
        fields = '__all__'
