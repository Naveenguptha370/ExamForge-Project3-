from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Timetable, TimetableEntry, SchedulingConflict, TimetableRevision
from .serializers import TimetableSerializer, TimetableEntrySerializer, SchedulingConflictSerializer
from .solver import TimetableSchedulerEngine

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.select_related('exam_session', 'approved_by').prefetch_related('entries', 'conflicts').all()
    serializer_class = TimetableSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def generate(self, request):
        session_id = request.data.get('exam_session_id')
        if not session_id:
            return Response({'error': 'exam_session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        engine = TimetableSchedulerEngine(session_id)
        result = engine.solve()

        timetable = Timetable.objects.get(exam_session_id=session_id)
        data = TimetableSerializer(timetable).data
        return Response({
            'solver_result': result,
            'timetable': data
        })

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        timetable = self.get_object()
        if timetable.conflict_count > 0:
            return Response({'error': 'Cannot approve timetable with active conflicts. Resolve clashes first.'}, status=status.HTTP_400_BAD_REQUEST)

        timetable.status = Timetable.Status.APPROVED
        timetable.approved_by = request.user
        timetable.approved_at = timezone.now()
        timetable.save()
        return Response({'message': f'Timetable for {timetable.exam_session.session_code} has been approved.'})

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        timetable = self.get_object()
        if timetable.status != Timetable.Status.APPROVED and timetable.conflict_count > 0:
            return Response({'error': 'Only approved conflict-free timetables can be published.'}, status=status.HTTP_400_BAD_REQUEST)

        timetable.status = Timetable.Status.PUBLISHED
        timetable.published_at = timezone.now()
        timetable.save()

        # Update session status
        timetable.exam_session.status = 'PUBLISHED'
        timetable.exam_session.save()

        return Response({'message': f'Timetable successfully published. Students and faculty can now view their schedules.'})

    @action(detail=True, methods=['post'])
    def manual_adjust(self, request, pk=None):
        timetable = self.get_object()
        entry_id = request.data.get('entry_id')
        new_date = request.data.get('exam_date')
        new_slot_id = request.data.get('time_slot_id')

        entry = TimetableEntry.objects.filter(timetable=timetable, id=entry_id).first()
        if not entry:
            return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

        entry.exam_date = new_date
        entry.time_slot_id = new_slot_id
        entry.is_manually_adjusted = True
        entry.save()

        # Update exam subject planned date
        entry.exam_subject.planned_date = new_date
        entry.exam_subject.time_slot_id = new_slot_id
        entry.exam_subject.save()

        return Response({'message': 'Timetable entry adjusted successfully.', 'entry': TimetableEntrySerializer(entry).data})


class TimetableEntryViewSet(viewsets.ModelViewSet):
    queryset = TimetableEntry.objects.select_related('timetable', 'exam_subject', 'time_slot').all()
    serializer_class = TimetableEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        session_id = self.request.query_params.get('exam_session')
        date = self.request.query_params.get('date')
        if session_id:
            qs = qs.filter(timetable__exam_session_id=session_id)
        if date:
            qs = qs.filter(exam_date=date)
        return qs
