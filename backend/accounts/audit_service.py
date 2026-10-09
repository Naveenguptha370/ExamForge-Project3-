"""
ExamForge - Audit Trail & Security Diff Service
Member 1: Authentication & User Management
"""
import json
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from django.db import models

class AuditTrailService:
    @staticmethod
    def calculate_diff(old_state: Dict[str, Any], new_state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        diff = {}
        all_keys = set(old_state.keys()).union(set(new_state.keys()))
        for key in all_keys:
            if key in ('password', '_state', 'created_at', 'updated_at'):
                continue
            old_val = old_state.get(key)
            new_val = new_state.get(key)
            if old_val != new_val:
                diff[key] = {'before': str(old_val), 'after': str(new_val)}
        return diff
