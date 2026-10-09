from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from .models import FacultyAvailability, FacultyLeave, FacultyProfile


class FacultyPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.edu',
            password='Admin!StrongPassword123',
            role=User.Role.ADMIN,
            is_staff=True,
        )
        self.faculty_user = User.objects.create_user(
            username='faculty',
            email='faculty@example.edu',
            password='Faculty!StrongPassword123',
            role=User.Role.FACULTY,
        )
        self.other_faculty_user = User.objects.create_user(
            username='other-faculty',
            email='other@example.edu',
            password='Other!StrongPassword123',
            role=User.Role.FACULTY,
        )
        self.faculty = FacultyProfile.objects.create(
            user=self.faculty_user,
            faculty_id='FAC-001',
            department='Science',
            designation='Professor',
            email='faculty@example.edu',
        )
        self.other_faculty = FacultyProfile.objects.create(
            user=self.other_faculty_user,
            faculty_id='FAC-002',
            department='Arts',
            designation='Lecturer',
            email='other@example.edu',
        )

    def test_faculty_can_only_read_own_profile_and_leave(self):
        own_leave = FacultyLeave.objects.create(
            faculty=self.faculty,
            start_date='2026-11-01',
            end_date='2026-11-02',
            reason='Personal leave',
        )
        FacultyLeave.objects.create(
            faculty=self.other_faculty,
            start_date='2026-11-03',
            end_date='2026-11-04',
            reason='Other leave',
        )
        self.client.force_authenticate(self.faculty_user)

        profile_response = self.client.get('/api/faculty/profiles/')
        other_profile_response = self.client.get(f'/api/faculty/profiles/{self.other_faculty.pk}/')
        leave_response = self.client.get('/api/faculty/leave/')

        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual([item['id'] for item in profile_response.data['results']], [self.faculty.pk])
        self.assertEqual(other_profile_response.status_code, 404)
        self.assertEqual([item['id'] for item in leave_response.data['results']], [own_leave.pk])

    def test_faculty_cannot_write_profiles_or_availability_or_other_faculty_leave(self):
        availability = FacultyAvailability.objects.create(
            faculty=self.faculty,
            day_of_week='MONDAY',
            start_time='09:00',
            end_time='17:00',
        )
        self.client.force_authenticate(self.faculty_user)

        profile_response = self.client.patch(
            f'/api/faculty/profiles/{self.faculty.pk}/',
            {'department': 'Changed'},
        )
        availability_response = self.client.patch(
            f'/api/faculty/availability/{availability.pk}/',
            {'is_available': False},
        )
        leave_response = self.client.post('/api/faculty/leave/', {
            'faculty': self.other_faculty.pk,
            'start_date': '2026-11-05',
            'end_date': '2026-11-06',
            'reason': 'Unauthorized leave',
        })

        self.assertEqual(profile_response.status_code, 403)
        self.assertEqual(availability_response.status_code, 403)
        self.assertEqual(leave_response.status_code, 400)
        self.assertEqual(FacultyLeave.objects.count(), 0)

    def test_admin_can_manage_faculty_and_view_dashboard(self):
        self.client.force_authenticate(self.admin)

        profile_response = self.client.get('/api/faculty/profiles/')
        dashboard_response = self.client.get('/api/faculty/dashboard/')

        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(profile_response.data['count'], 2)
        self.assertEqual(dashboard_response.status_code, 200)
