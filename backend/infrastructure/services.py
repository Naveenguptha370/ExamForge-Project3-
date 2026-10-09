from django.db import transaction
from django.db.models import Q
from .models import Room, RoomMaintenance, RoomAssignment
from seating.models import Seat
from examinations.models import Examination


def ensure_room_seats(room: Room):
    """
    Generates or synchronizes physical Seat objects for a Room based on its rows and columns.
    Prunes out-of-bounds seats if dimensions were reduced, updates is_usable flag,
    and creates missing seat coordinates.
    """
    with transaction.atomic():
        # 1. Prune obsolete seats outside current rows and columns
        Seat.objects.filter(room=room).filter(
            Q(row_index__gt=room.rows) | Q(col_index__gt=room.columns)
        ).delete()

        existing_seats = {(s.row_index, s.col_index): s for s in Seat.objects.filter(room=room)}
        
        # Row letters: A, B, C... or R1, R2
        def get_row_char(r):
            if r <= 26:
                return chr(64 + r)
            return f"R{r}"

        seats_to_create = []
        seats_to_update = []

        for r in range(1, room.rows + 1):
            row_prefix = get_row_char(r)
            for c in range(1, room.columns + 1):
                label = f"{row_prefix}{c}"
                index = (r - 1) * room.columns + c
                is_usable = index <= room.usable_capacity

                if (r, c) in existing_seats:
                    s = existing_seats[(r, c)]
                    if s.seat_label != label or s.is_usable != is_usable:
                        s.seat_label = label
                        s.is_usable = is_usable
                        seats_to_update.append(s)
                else:
                    seats_to_create.append(
                        Seat(
                            room=room,
                            row_index=r,
                            col_index=c,
                            seat_label=label,
                            is_usable=is_usable
                        )
                    )

        if seats_to_create:
            Seat.objects.bulk_create(seats_to_create)
        if seats_to_update:
            Seat.objects.bulk_update(seats_to_update, ['seat_label', 'is_usable'])


def check_room_availability(room_id, exam_date, time_slot_id, exclude_assignment_id=None):
    """
    Checks if a room is available on a specific date and time slot:
    1. Not under maintenance.
    2. Not assigned to another examination on the same date and time slot.
    Returns: (is_available: bool, conflict_reason: str or None)
    """
    # 1. Maintenance check
    active_maint = RoomMaintenance.objects.filter(
        room_id=room_id,
        is_resolved=False,
        start_date__lte=exam_date,
        end_date__gte=exam_date
    ).first()

    if active_maint:
        return False, f"Room is under maintenance from {active_maint.start_date} to {active_maint.end_date}: {active_maint.reason}"

    # 2. Overlapping exam check
    overlapping_assignments = RoomAssignment.objects.filter(
        room_id=room_id,
        examination__exam_date=exam_date,
        examination__time_slot_id=time_slot_id
    )
    if exclude_assignment_id:
        overlapping_assignments = overlapping_assignments.exclude(id=exclude_assignment_id)

    overlap = overlapping_assignments.select_related('examination__subject').first()
    if overlap:
        return False, f"Room is already assigned to {overlap.examination.subject.code} on {exam_date} during this time slot."

    return True, None


def get_room_utilization_stats():
    """
    Calculates institutional room utilization metrics.
    """
    rooms = Room.objects.filter(is_active=True).select_related('building')
    total_rooms = rooms.count()
    total_physical_capacity = sum(r.capacity for r in rooms)
    total_usable_capacity = sum(r.usable_capacity for r in rooms)

    # Currently occupied rooms (active room assignments)
    active_assignments = RoomAssignment.objects.filter(status__in=['reserved', 'active'])
    occupied_room_ids = set(active_assignments.values_list('room_id', flat=True))
    occupied_rooms_count = len(occupied_room_ids)

    # In maintenance
    maintenance_room_ids = set(RoomMaintenance.objects.filter(is_resolved=False).values_list('room_id', flat=True))
    maintenance_rooms_count = len(maintenance_room_ids)

    available_rooms_count = max(0, total_rooms - occupied_rooms_count - maintenance_rooms_count)

    utilization_rate = round((occupied_rooms_count / total_rooms * 100), 1) if total_rooms > 0 else 0

    return {
        'total_rooms': total_rooms,
        'total_physical_capacity': total_physical_capacity,
        'total_usable_capacity': total_usable_capacity,
        'occupied_rooms_count': occupied_rooms_count,
        'available_rooms_count': available_rooms_count,
        'maintenance_rooms_count': maintenance_rooms_count,
        'utilization_rate_percent': utilization_rate
    }
