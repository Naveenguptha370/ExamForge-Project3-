from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Building, ExaminationRoom, RoomAvailability
from .serializers import BuildingSerializer, ExaminationRoomSerializer, RoomAvailabilitySerializer

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExaminationRoomViewSet(viewsets.ModelViewSet):
    queryset = ExaminationRoom.objects.select_related('building').all()
    serializer_class = ExaminationRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        building_id = self.request.query_params.get('building')
        status_val = self.request.query_params.get('status')
        min_cap = self.request.query_params.get('min_capacity')
        search = self.request.query_params.get('search')

        if building_id:
            qs = qs.filter(building_id=building_id)
        if status_val:
            qs = qs.filter(status=status_val)
        if min_cap:
            qs = qs.filter(usable_capacity__gte=int(min_cap))
        if search:
            qs = qs.filter(room_number__icontains=search)
        return qs

    @action(detail=False, methods=['get'])
    def summary(self, request):
        total_rooms = ExaminationRoom.objects.count()
        available_rooms = ExaminationRoom.objects.filter(status='AVAILABLE').count()
        total_capacity = ExaminationRoom.objects.filter(status='AVAILABLE').aggregate(Sum('usable_capacity'))['usable_capacity__sum'] or 0
        return Response({
            'total_rooms': total_rooms,
            'available_rooms': available_rooms,
            'maintenance_rooms': total_rooms - available_rooms,
            'total_usable_capacity': total_capacity
        })


class RoomAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = RoomAvailability.objects.select_related('room').all()
    serializer_class = RoomAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]
