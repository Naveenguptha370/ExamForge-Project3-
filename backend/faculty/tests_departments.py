"""
Unit tests for Member 1 Department Directory Manager.
"""
from django.test import TestCase
from accounts.models import User
from faculty.models import FacultyProfile
from faculty.department_directory import DepartmentDirectoryManager

class DepartmentDirectoryTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='fac1', email='f1@examforge.edu')
        self.user2 = User.objects.create_user(username='fac2', email='f2@examforge.edu')
        self.p1 = FacultyProfile.objects.create(
            user=self.user1, faculty_id='FAC-CS-01', department='Computer Science',
            designation='Professor', status='ACTIVE', email='f1@examforge.edu'
        )
        self.p2 = FacultyProfile.objects.create(
            user=self.user2, faculty_id='FAC-CS-02', department='Computer Science',
            designation='Assistant Professor', status='ON_LEAVE', email='f2@examforge.edu'
        )

    def test_department_roster_retrieval(self):
        roster = DepartmentDirectoryManager.get_department_roster('Computer Science')
        self.assertEqual(len(roster), 2)
        ids = [item['faculty_id'] for item in roster]
        self.assertIn('FAC-CS-01', ids)
        self.assertIn('FAC-CS-02', ids)

    def test_search_faculty(self):
        results = DepartmentDirectoryManager.search_faculty('CS-01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['faculty_id'], 'FAC-CS-01')
