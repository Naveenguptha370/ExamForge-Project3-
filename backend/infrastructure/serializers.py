from rest_framework import serializers
from .models import Building, Room, RoomMaintenance, RoomAssignment
from seating.models import Seat


class BuildingSerializer(serializers.ModelSerializer):
    rooms_count = serializers.IntegerField(source='rooms.count', read_only=True)

    class Meta:
        model = Building
        fields = ['id', 'code', 'name', 'campus_zone', 'total_floors', 'has_elevator', 'rooms_count']


class SeatSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'row_index', 'col_index', 'seat_label', 'is_usable']


class RoomSerializer(serializers.ModelSerializer):
    building_code = serializers.CharField(source='building.code', read_only=True)
    building_name = serializers.CharField(source='building.name', read_only=True)
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    grid_total = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id', 'room_number', 'building', 'building_code', 'building_name',
            'floor', 'room_type', 'room_type_display', 'capacity', 'usable_capacity',
            'rows', 'columns', 'grid_total', 'is_accessible', 'has_cctv',
            'has_air_conditioning', 'is_active', 'notes', 'created_at'
        ]

    def get_grid_total(self, obj):
        return obj.rows * obj.columns

    def validate(self, data):
        capacity = data.get('capacity', getattr(self.instance, 'capacity', 0))
        usable = data.get('usable_capacity', getattr(self.instance, 'usable_capacity', 0))
        rows = data.get('rows', getattr(self.instance, 'rows', 1))
        columns = data.get('columns', getattr(self.instance, 'columns', 1))

        if usable > capacity:
            raise serializers.ValidationError({"usable_capacity": "Usable capacity cannot exceed total physical capacity."})
        if rows * columns < usable:
            raise serializers.ValidationError({"usable_capacity": f"Grid size ({rows}x{columns}={rows*columns}) cannot be less than usable capacity ({usable})."})
        return data


class RoomMaintenanceSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='room.building.name', read_only=True)

    class Meta:
        model = RoomMaintenance
        fields = ['id', 'room', 'room_number', 'building_name', 'start_date', 'end_date', 'reason', 'is_resolved', 'created_at']


class RoomAssignmentSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='room.building.name', read_only=True)
    usable_capacity = serializers.IntegerField(source='room.usable_capacity', read_only=True)
    subject_code = serializers.CharField(source='examination.subject.code', read_only=True)
    subject_name = serializers.CharField(source='examination.subject.name', read_only=True)
    exam_date = serializers.DateField(source='examination.exam_date', read_only=True)
    time_slot_name = serializers.CharField(source='examination.time_slot.name', read_only=True)

    class Meta:
        model = RoomAssignment
        fields = [
            'id', 'examination', 'room', 'room_number', 'building_name',
            'usable_capacity', 'subject_code', 'subject_name', 'exam_date',
            'time_slot_name', 'allotted_students_count', 'status', 'assigned_at'
        ]
