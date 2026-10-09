"""
Unit tests for Member 1 Compliance Verification Pipeline.
"""
from django.test import TestCase
from faculty.compliance_verification import ComplianceVerificationPipeline

class ComplianceVerificationTests(TestCase):
    def test_full_compliance(self):
        docs = [
            'GOVERNMENT_PHOTO_ID',
            'HIGHEST_DEGREE_CERTIFICATE',
            'UNIVERSITY_APPOINTMENT_LETTER',
            'INVIGILATOR_CODE_OF_CONDUCT_SIGNATURE'
        ]
        res = ComplianceVerificationPipeline.check_compliance_status(docs)
        self.assertTrue(res['is_compliant'])
        self.assertEqual(res['compliance_score'], 100.0)
        self.assertEqual(len(res['missing_documents']), 0)

    def test_partial_compliance(self):
        docs = ['GOVERNMENT_PHOTO_ID']
        res = ComplianceVerificationPipeline.check_compliance_status(docs)
        self.assertFalse(res['is_compliant'])
        self.assertEqual(res['compliance_score'], 25.0)
        self.assertEqual(len(res['missing_documents']), 3)
