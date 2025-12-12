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
from datetime import date, datetime, timedelta
from typing import Tuple

_ISO_DATE_RE = re.compile(r"^\s*(\d{4})-(\d{2})-(\d{2})\s*$")


def _parse_iso_date_strict(s: str) -> Optional[date]:
    """
    Parse an ISO date string
    """
    if not isinstance(s, str):
        return None

    m = _ISO_DATE_RE.fullmatch(s)
    if not m:
        return None
    try:
        year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return date(year, month, day)
    except ValueError:
        return None


def validate_appointment_date(date_str) -> Tuple[bool, str]:
    """
    Validate appointment_date
    """
    if date_str is None:
        return False, "Appointment date is required"

    if not isinstance(date_str, str):
        return False, "Appointment date must be a string in YYYY-MM-DD format"

    parsed = _parse_iso_date_strict(date_str)
    if parsed is None:
        return False, "Appointment date must be a valid date in YYYY-MM-DD format"

    today = date.today()
    if parsed <= today:
        return False, "Appointment date must be in the future"

    max_allowed = today + timedelta(days=90)
    if parsed > max_allowed:
        return False, "Appointment date must be within 90 days from today"

    return True, ""


# --- FROM PART III ---

_SQL_XSS_REG = re.compile(
    r"(?:<\s*script\b|<[^>]*on\w+\s*=|--\s+|;\s*(?:DROP|DELETE|UPDATE|INSERT)\b|\bDROP\s+TABLE\b|\bSELECT\b.*\bFROM\b)",
    flags=re.IGNORECASE
)
_PHONE_FORMATS = [
    re.compile(r"^\d{3}-\d{3}-\d{4}$"),       # XXX-XXX-XXXX
    re.compile(r"^\(\d{3}\)\s?\d{3}-\d{4}$"), # (XXX) XXX-XXXX or (XXX)XXX-XXXX
    re.compile(r"^\d{3}\.\d{3}\.\d{4}$"),     # XXX.XXX.XXXX
    re.compile(r"^\d{10}$"),                  # XXXXXXXXXX
]

def validate_phone_number(phone) -> Tuple[bool, str]:
    """
    Validate phone number
    """
    if phone is None:
        return False, "Phone number is required"
    
    if not isinstance(phone, str):
        return False, "Phone number must be a string"
    
    phone_str = phone.strip()
    
    if len(phone_str) == 0:
        return False, "Phone number must not be empty"
    
    if _SQL_XSS_REG.search(phone_str):
        return False, "Phone number contains invalid characters"
    
    if any(c.isalpha() for c in phone_str):
        return False, "Phone number must not contain letters"
    
    dangerous_chars = ['&', '|', ';', '$', '`', '"', "'", '\\', '/', '*', '#', '!', '?', '=', '+']
    if any(char in phone_str for char in dangerous_chars):
        return False, "Phone number contains invalid characters"
    
    if any(ord(c) < 32 for c in phone_str if c not in ' '):
        return False, "Phone number contains invalid control characters"
    
    if phone_str.startswith('+'):
        return False, "Phone number must be in US format (no country code)"
    
    if phone_str.startswith('1-') or phone_str.startswith('1 '):
        return False, "Phone number must be in US format (no country code prefix)"
    
    extension_indicators = ['ext', 'x', 'extension', ',']
    phone_lower = phone_str.lower()
    if any(indicator in phone_lower for indicator in extension_indicators):
        return False, "Phone number must not include extensions"
    
    matches_format = False
    for pattern in _PHONE_FORMATS:
        if pattern.match(phone_str):
            matches_format = True
            break
    
    if not matches_format:
        return False, "Phone number must be in a valid US format: XXX-XXX-XXXX, (XXX) XXX-XXXX, XXX.XXX.XXXX, or XXXXXXXXXX"
    
    digits_only = ''.join(c for c in phone_str if c.isdigit())
    
    if len(digits_only) != 10:
        return False, f"Phone number must contain exactly 10 digits (found {len(digits_only)})"
    
    area_code = digits_only[:3]
    if area_code[0] in ['0', '1']:
        return False, "Invalid area code (cannot start with 0 or 1)"
    
    return True, ""


# --- FROM PART II ---

MAX_EMAIL_LENGTH = 100
MIN_EMAIL_LENGTH = 3
_LOCAL_PART_ATOM_RE = re.compile(r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+$")
_DOMAIN_LABEL_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")
_SQL_XSS_RE = re.compile(
    r"(?:<\s*script\b|<[^>]*on\w+\s*=|--\s+|;\s*(?:DROP|DELETE|UPDATE|INSERT)\b|\bDROP\s+TABLE\b|\bSELECT\b.*\bFROM\b)",
    flags=re.IGNORECASE
)


def validate_patient_email(value) -> Tuple[bool, str]:
    """
    Validate an email address
    """
    if value is None:
        return False, "Email is required"

    if not isinstance(value, str):
        return False, "Email must be a string"

    email = value.strip()

    if len(email) == 0:
        return False, "Email must not be empty"

    if len(email) < MIN_EMAIL_LENGTH:
        return False, "Email is too short"

    if len(email) > MAX_EMAIL_LENGTH:
        return False, "Email must be at most 100 characters"

    if _SQL_XSS_RE.search(email):
        return False, "Email contains invalid characters"

    if "@" not in email:
        return False, "Email must contain a single @ character"
    local_part, domain = email.rsplit("@", 1)

    if not local_part or not domain:
        return False, "Email must have both local part and domain"

    if len(local_part) > 64:
        return False, "Local part is too long"

    if local_part[0] == "." or local_part[-1] == ".":
        return False, "Local part must not start or end with a dot"
    if ".." in local_part:
        return False, "Local part must not contain consecutive dots"

    if not _LOCAL_PART_ATOM_RE.match(local_part):
        return False, "Local part contains invalid characters"

    domain = domain.strip()
    if "." not in domain:
        return False, "Domain must contain a top-level domain (e.g., example.com)"

    try:
        domain_ascii = domain.encode("idna").decode("ascii")
    except Exception:
        return False, "Domain contains invalid characters"

    if domain_ascii.startswith(".") or domain_ascii.endswith("."):
        return False, "Domain must not start or end with a dot"
    if ".." in domain_ascii:
        return False, "Domain must not contain consecutive dots"

    labels = domain_ascii.split(".")
    tld = labels[-1]
    if len(tld) < 2:
        return False, "Top-level domain is invalid"
    if not (tld[0].isalpha() and tld[-1].isalnum() and all(c.isalnum() or c == '-' for c in tld)):
        return False, "Top-level domain is invalid"

    for label in labels:
        if len(label) == 0 or len(label) > 63:
            return False, "Domain label has invalid length"
        if not _DOMAIN_LABEL_RE.match(label):
            return False, "Domain contains invalid characters or structure"

    if len(local_part) + 1 + len(domain_ascii) > MAX_EMAIL_LENGTH:
        return False, "Email must be at most 100 characters"

    return True, ""


# --- FROM PART I ---

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
