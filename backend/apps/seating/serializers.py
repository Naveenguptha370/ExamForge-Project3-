from rest_framework import serializers
from .models import Seat, SeatingPlan, SeatAllocation

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'


class SeatAllocationSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_no', read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_reg = serializers.CharField(source='student.registration_no', read_only=True)
    seat_label = serializers.CharField(source='seat.seat_label', read_only=True)
    row_num = serializers.IntegerField(source='seat.row_num', read_only=True)
    col_num = serializers.IntegerField(source='seat.col_num', read_only=True)
    room_number = serializers.CharField(source='seating_plan.room.room_number', read_only=True)

    class Meta:
        model = SeatAllocation
        fields = '__all__'


class SeatingPlanSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='exam_subject.subject.code', read_only=True)
    subject_name = serializers.CharField(source='exam_subject.subject.name', read_only=True)
    exam_date = serializers.DateField(source='exam_subject.planned_date', read_only=True)
    slot_name = serializers.CharField(source='exam_subject.time_slot.name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='room.building.name', read_only=True)
    allocations = SeatAllocationSerializer(many=True, read_only=True)

    class Meta:
        model = SeatingPlan
        fields = '__all__'
