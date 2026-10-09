"""
ExamForge - Institutional Directory & Identity Provider Connector
Member 1: Authentication & User Management
"""
from typing import Dict, Any, Optional

class MockLDAPDirectoryConnector:
    """Simulates enterprise Active Directory / OpenLDAP university synchronization."""
    DEFAULT_CONFIG = {
        'server_uri': 'ldap://directory.examforge.internal:389',
        'bind_dn': 'cn=ExamForgeService,ou=Services,dc=examforge,dc=edu',
        'search_base': 'ou=FacultyAndStaff,dc=examforge,dc=edu'
    }

    @classmethod
    def test_connection(cls) -> bool:
        return True

    @classmethod
    def map_ldap_attributes(cls, ldap_entry: Dict[str, Any]) -> Dict[str, str]:
        return {
            'username': ldap_entry.get('sAMAccountName', ''),
            'email': ldap_entry.get('mail', ''),
            'first_name': ldap_entry.get('givenName', ''),
            'last_name': ldap_entry.get('sn', ''),
            'department': ldap_entry.get('department', 'General Academics'),
            'designation': ldap_entry.get('title', 'Faculty Member')
        }
