from rest_framework import serializers
from .models import Building, ExaminationRoom, RoomAvailability

class BuildingSerializer(serializers.ModelSerializer):
    rooms_count = serializers.IntegerField(source='rooms.count', read_only=True)

    class Meta:
        model = Building
        fields = '__all__'


class ExaminationRoomSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source='building.name', read_only=True)
    building_code = serializers.CharField(source='building.code', read_only=True)
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)

    class Meta:
        model = ExaminationRoom
        fields = '__all__'


class RoomAvailabilitySerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room.room_number', read_only=True)

    class Meta:
        model = RoomAvailability
        fields = '__all__'
