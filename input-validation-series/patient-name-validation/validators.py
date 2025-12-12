#!/usr/bin/env python3
"""
validators.py

This is a reference implementation.

Before deploying the final challenge, replace or strip this implementation
so learners receive only the starter scaffolding.

Each validator returns a tuple: (is_valid: bool, error_message: str).
"""

from __future__ import annotations

import re
from typing import Tuple

_NAME_ALLOW_RE = re.compile(r"^[A-Za-z\s'-]+$")
_SQL_INJECTION_INDICATORS = re.compile(
    r"(;|--|\bDROP\b|\bTABLE\b|\bSELECT\b|\bDELETE\b|\bINSERT\b|\bUPDATE\b)",
    flags=re.IGNORECASE,
)
_XSS_INDICATORS = re.compile(r"[<>]")


def validate_patient_name(name) -> Tuple[bool, str]:
    """
    Validate patient name
    """
    if name is None:
        return False, "Name is required"

    if not isinstance(name, str):
        return False, "Name must be a string"

    name_str = name.strip()
    if len(name_str) == 0:
        return False, "Name must not be empty"
    if len(name_str) < 2:
        return False, "Name must be at least 2 characters"
    if len(name_str) > 50:
        return False, "Name must be no more than 50 characters"

    if _XSS_INDICATORS.search(name_str):
        return False, "Name contains invalid characters"

    if _SQL_INJECTION_INDICATORS.search(name_str):
        return False, "Name contains invalid patterns"

    if not _NAME_ALLOW_RE.match(name_str):
        return False, "Name contains invalid characters (allowed: letters, spaces, hyphen, apostrophe)"

    return True, ""
