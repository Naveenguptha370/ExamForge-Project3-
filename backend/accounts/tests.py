from django.test import TestCase
from rest_framework.test import APIClient

from .models import AuditLog, User


class UserManagementPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.edu',
            password='Admin!StrongPassword123',
            role=User.Role.ADMIN,
            is_staff=True,
        )
        self.faculty = User.objects.create_user(
            username='faculty',
            email='faculty@example.edu',
            password='Faculty!StrongPassword123',
            role=User.Role.FACULTY,
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.edu',
            password='Student!StrongPassword123',
            role=User.Role.STUDENT,
        )

    def test_unauthenticated_user_cannot_list_users(self):
        response = self.client.get('/api/auth/users/')

        self.assertEqual(response.status_code, 403)

    def test_non_admin_user_can_only_list_and_retrieve_their_own_account(self):
        self.client.force_authenticate(self.faculty)

        list_response = self.client.get('/api/auth/users/')
        detail_response = self.client.get(f'/api/auth/users/{self.student.pk}/')
        self_detail_response = self.client.get(f'/api/auth/users/{self.faculty.pk}/')

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual([item['id'] for item in list_response.data['results']], [self.faculty.pk])
        self.assertEqual(detail_response.status_code, 404)
        self.assertEqual(self_detail_response.status_code, 200)

    def test_non_admin_cannot_create_accounts_or_access_admin_actions(self):
        self.client.force_authenticate(self.faculty)

        create_response = self.client.post('/api/auth/users/', {
            'username': 'new-user',
            'email': 'new@example.edu',
            'password': 'New!StrongPassword123',
            'role': User.Role.STUDENT,
        })
        dashboard_response = self.client.get('/api/auth/dashboard/')
        reset_response = self.client.post('/api/auth/users/reset-password/', {
            'username': 'student',
            'new_password': 'Changed!StrongPassword123',
        })
        deactivate_response = self.client.post('/api/auth/users/deactivate/', {
            'user_id': self.student.pk,
        })

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(dashboard_response.status_code, 403)
        self.assertEqual(reset_response.status_code, 403)
        self.assertEqual(deactivate_response.status_code, 403)
        self.student.refresh_from_db()
        self.assertTrue(self.student.is_active)

    def test_admin_can_list_accounts_and_deactivation_is_audited(self):
        self.client.force_authenticate(self.admin)

        list_response = self.client.get('/api/auth/users/')
        deactivate_response = self.client.post('/api/auth/users/deactivate/', {
            'user_id': self.student.pk,
        })

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data['count'], 3)
        self.assertEqual(deactivate_response.status_code, 200)
        self.student.refresh_from_db()
        self.assertFalse(self.student.is_active)
        self.assertEqual(self.student.status, User.Status.INACTIVE)
        self.assertTrue(AuditLog.objects.filter(
            actor=self.admin,
            action='user_deactivated',
            object_id=str(self.student.pk),
        ).exists())

    def test_admin_cannot_deactivate_their_own_account(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post('/api/auth/users/deactivate/', {
            'user_id': self.admin.pk,
        })

        self.assertEqual(response.status_code, 400)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)
