from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import Building, Room, RoomMaintenance, RoomAssignment
from .serializers import (
    BuildingSerializer, RoomSerializer,
    RoomMaintenanceSerializer, RoomAssignmentSerializer
)
from .services import ensure_room_seats, check_room_availability, get_room_utilization_stats


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all().order_by('code')
    serializer_class = BuildingSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().select_related('building')
    serializer_class = RoomSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        building_id = self.request.query_params.get('building')
        room_type = self.request.query_params.get('room_type')
        floor = self.request.query_params.get('floor')
        is_accessible = self.request.query_params.get('is_accessible')
        search = self.request.query_params.get('search')

        if building_id:
            qs = qs.filter(building_id=building_id)
        if room_type:
            qs = qs.filter(room_type=room_type)
        if floor is not None and floor != '':
            qs = qs.filter(floor=floor)
        if is_accessible is not None and is_accessible != '':
            qs = qs.filter(is_accessible=(is_accessible.lower() == 'true'))
        if search:
            qs = qs.filter(
                Q(room_number__icontains=search) |
                Q(building__name__icontains=search) |
                Q(building__code__icontains=search)
            )
        return qs

    def perform_create(self, serializer):
        room = serializer.save()
        ensure_room_seats(room)

    def perform_update(self, serializer):
        room = serializer.save()
        ensure_room_seats(room)

    @action(detail=True, methods=['get'])
    def seats(self, request, pk=None):
        room = self.get_object()
        seats = room.seats.all().order_by('row_index', 'col_index')
        from .serializers import SeatSimpleSerializer
        serializer = SeatSimpleSerializer(seats, many=True)
        return Response({
            'room_id': room.id,
            'room_number': room.room_number,
            'building': room.building.name,
            'rows': room.rows,
            'columns': room.columns,
            'capacity': room.capacity,
            'usable_capacity': room.usable_capacity,
            'seats': serializer.data
        })

    @action(detail=True, methods=['get'])
    def check_availability(self, request, pk=None):
        room = self.get_object()
        exam_date = request.query_params.get('exam_date')
        time_slot_id = request.query_params.get('time_slot_id')
        if not exam_date or not time_slot_id:
            return Response({'error': 'exam_date and time_slot_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        is_avail, reason = check_room_availability(room.id, exam_date, time_slot_id)
        return Response({
            'room_id': room.id,
            'is_available': is_avail,
            'reason': reason
        })


class RoomMaintenanceViewSet(viewsets.ModelViewSet):
    queryset = RoomMaintenance.objects.all().select_related('room', 'room__building').order_by('-start_date')
    serializer_class = RoomMaintenanceSerializer


class RoomAssignmentViewSet(viewsets.ModelViewSet):
    queryset = RoomAssignment.objects.all().select_related('examination', 'examination__subject', 'room', 'room__building').order_by('-assigned_at')
    serializer_class = RoomAssignmentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        exam_id = self.request.query_params.get('examination')
        if exam_id:
            qs = qs.filter(examination_id=exam_id)
        return qs


class RoomUtilizationView(APIView):
    def get(self, request):
        stats = get_room_utilization_stats()
        # Also include room breakdown
        rooms = Room.objects.filter(is_active=True).select_related('building')
        room_list = []
        for r in rooms:
            in_maint = RoomMaintenance.objects.filter(room=r, is_resolved=False).exists()
            active_assign = RoomAssignment.objects.filter(room=r, status__in=['reserved', 'active']).first()
            room_list.append({
                'id': r.id,
                'room_number': r.room_number,
                'building': r.building.name,
                'building_code': r.building.code,
                'floor': r.floor,
                'room_type': r.get_room_type_display(),
                'capacity': r.capacity,
                'usable_capacity': r.usable_capacity,
                'status': 'Maintenance' if in_maint else ('In Use' if active_assign else 'Available'),
                'current_exam': active_assign.examination.subject.code if active_assign else None,
                'is_accessible': r.is_accessible,
            })
        return Response({
            'overview': stats,
            'rooms': room_list
        })
