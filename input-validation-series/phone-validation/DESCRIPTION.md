**Assignee:** You

**Priority:** High

**Status:** To Do

**Deliverable:** Updated `validators.py`

**ETA:** End of day

#### Background
The third challenge focuses on *phone number validation*, a critical component of contact information security. Phone numbers are frequently used for multi-factor authentication, emergency contacts, and communication, making their integrity essential.

The current `appointment_api.py` accepts `phone_number` without validation, allowing malicious strings like `ABC-DEF-GHIJ`, `555'; DROP TABLE--`, or invalid formats that could break downstream systems. This creates security vulnerabilities and data quality issues.

#### Objective
Implement a robust validator for `phone_number` in `validators.py` that accepts standard US phone number formats while preventing injection attacks and malformed data.

#### Accepted Formats
Your validator must accept standard US formats, including:
- `XXX-XXX-XXXX` (hyphen-separated): `555-123-4567`
- `(XXX)XXX-XXXX` (parentheses): `(555)123-4567`
- `XXXXXXXXXX` (no separators): `5551234567`

#### Acceptance Criteria
- Valid phone numbers in any accepted format are accepted (return `201`)
- All malformed, invalid, or malicious inputs are rejected (`400`)
- Checker completes successfully and prints the flag
