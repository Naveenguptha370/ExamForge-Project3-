import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User, UserActivityLog
from apps.faculty.models import FacultyProfile, FacultyAvailability, FacultyLeave
from apps.academics.models import Department

User = get_user_model()

class Member1AuthFacultyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dept = Department.objects.create(code='CSE', name='Computer Science')

        self.admin = User.objects.create_user(
            username='admin_test',
            password='Password123!',
            role=User.Role.ADMIN
        )
        self.faculty_user = User.objects.create_user(
            username='faculty_test',
            password='Password123!',
            role=User.Role.FACULTY
        )
        self.faculty_profile = FacultyProfile.objects.create(
            user=self.faculty_user,
            employee_id='FAC-TEST-01',
            department=self.dept,
            designation=FacultyProfile.Designation.ASST_PROFESSOR,
            phone='9999999999',
            max_duties_per_term=6
        )

    def test_login_success(self):
        response = self.client.post('/api/accounts/auth/login/', {
            'username': 'admin_test',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['role'], 'ADMIN')

    def test_login_invalid_credentials(self):
        response = self.client.post('/api/accounts/auth/login/', {
            'username': 'admin_test',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deactivated_account_login_prevented(self):
        self.faculty_user.is_active = False
        self.faculty_user.save()

        response = self.client.post('/api/accounts/auth/login/', {
            'username': 'faculty_test',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_profile_creation_and_summary(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/faculty/profiles/summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_faculty'], 1)
        self.assertEqual(response.data['available_faculty'], 1)

    def test_faculty_leave_approval(self):
        leave = FacultyLeave.objects.create(
            faculty=self.faculty_profile,
            start_date='2026-05-15',
            end_date='2026-05-17',
            reason='Attending IEEE Conference'
        )
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(f'/api/faculty/leaves/{leave.id}/approve/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        leave.refresh_from_db()
        self.assertEqual(leave.status, FacultyLeave.Status.APPROVED)
        self.assertEqual(leave.approved_by, self.admin)
