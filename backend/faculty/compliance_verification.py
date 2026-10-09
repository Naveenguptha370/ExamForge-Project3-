"""
ExamForge - Faculty Compliance & Document Verification
Member 1: Faculty Management
"""
from typing import Dict, Any, List

class ComplianceVerificationPipeline:
    """Verifies that faculty members hold verified statutory documentation."""
    REQUIRED_DOCUMENTS = [
        'GOVERNMENT_PHOTO_ID',
        'HIGHEST_DEGREE_CERTIFICATE',
        'UNIVERSITY_APPOINTMENT_LETTER',
        'INVIGILATOR_CODE_OF_CONDUCT_SIGNATURE'
    ]

    @classmethod
    def check_compliance_status(cls, submitted_docs: List[str]) -> Dict[str, Any]:
        missing = [doc for doc in cls.REQUIRED_DOCUMENTS if doc not in submitted_docs]
        is_compliant = len(missing) == 0
        return {
            'is_compliant': is_compliant,
            'compliance_score': round(((len(cls.REQUIRED_DOCUMENTS) - len(missing)) / len(cls.REQUIRED_DOCUMENTS)) * 100, 1),
            'missing_documents': missing
        }
