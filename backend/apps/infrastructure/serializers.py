from rest_framework import serializers
from .models import Block, Room, RoomAvailability

class BlockSerializer(serializers.ModelSerializer):
    rooms_count = serializers.IntegerField(source='rooms.count', read_only=True)

    class Meta:
        model = Block
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    block_code = serializers.CharField(source='block.code', read_only=True)
    block_name = serializers.CharField(source='block.name', read_only=True)
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class RoomAvailabilitySerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    block_code = serializers.CharField(source='room.block.code', read_only=True)

    class Meta:
        model = RoomAvailability
        fields = '__all__'
