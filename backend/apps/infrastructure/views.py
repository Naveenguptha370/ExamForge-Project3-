from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Block, Room, RoomAvailability
from .serializers import BlockSerializer, RoomSerializer, RoomAvailabilitySerializer
from apps.accounts.permissions import IsStaffOrAdmin, IsAdminUserRole

class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all().order_by('code')
    serializer_class = BlockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [IsAuthenticated()]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('block__code', 'room_number')
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['room_number', 'block__code', 'block__name']
    ordering_fields = ['room_number', 'usable_exam_capacity', 'floor_number']

    def get_queryset(self):
        qs = super().get_queryset()
        block = self.request.query_params.get('block')
        room_type = self.request.query_params.get('room_type')
        min_cap = self.request.query_params.get('min_capacity')
        is_active = self.request.query_params.get('is_active')

        if block:
            qs = qs.filter(block_id=block)
        if room_type:
            qs = qs.filter(room_type=room_type)
        if min_cap:
            qs = qs.filter(usable_exam_capacity__gte=min_cap)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]


class RoomAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = RoomAvailability.objects.all().order_by('date')
    serializer_class = RoomAvailabilitySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        room = self.request.query_params.get('room')
        date = self.request.query_params.get('date')
        if room:
            qs = qs.filter(room_id=room)
        if date:
            qs = qs.filter(date=date)
        return qs

    def get_permissions(self):
        return [IsAuthenticated()]
