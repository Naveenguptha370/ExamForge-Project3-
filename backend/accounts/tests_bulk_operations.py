"""
Unit tests for Member 1 Bulk Faculty Import Parser.
"""
from django.test import TestCase
from accounts.bulk_operations import BulkFacultyImportParser

class BulkOperationsTests(TestCase):
    def test_parse_valid_csv(self):
        sample_csv = "faculty_id,username,email,department,designation\nFAC-01,u1,u1@examforge.edu,CS,Professor\n"
        res = BulkFacultyImportParser.parse_csv(sample_csv)
        self.assertEqual(res['total_rows'], 1)
        self.assertEqual(res['valid_count'], 1)
        self.assertEqual(res['invalid_count'], 0)

    def test_parse_invalid_csv(self):
        sample_csv = "faculty_id,username,email,department,designation\nFAC-01,,bademail,CS,Professor\n"
        res = BulkFacultyImportParser.parse_csv(sample_csv)
        self.assertEqual(res['total_rows'], 1)
        self.assertEqual(res['valid_count'], 0)
        self.assertEqual(res['invalid_count'], 1)
