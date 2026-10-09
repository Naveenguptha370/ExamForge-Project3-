"""
ExamForge - Faculty Compliance & Document Verification
Member 1: Faculty Management
"""
from typing import Dict, Any, List

class ComplianceVerificationPipeline:
    REQUIRED_DOCUMENTS = ['PHOTO_ID', 'DEGREE_CERTIFICATE', 'APPOINTMENT_LETTER']

    @classmethod
    def check_compliance_status(cls, submitted_docs: List[str]) -> Dict[str, Any]:
        missing = [doc for doc in cls.REQUIRED_DOCUMENTS if doc not in submitted_docs]
        return {'is_compliant': len(missing) == 0, 'missing': missing}
