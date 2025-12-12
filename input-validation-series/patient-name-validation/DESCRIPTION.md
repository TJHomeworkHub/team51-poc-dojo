**Assignee:** You

**Priority:** High  

**Status:** To Do

**Deliverable:** Updated `validators.py`

**ETA:** End of day

#### Background  
The first challenge focuses on *patient name validation*, which represents a common real world attack surface where user-provided identifiers are leveraged for injection, XSS, or malformed-input exploitation.

The current `appointment_api.py` accepts `patient_name` with no validation, allowing for strings that could break downstream logic, create security vulnerabilities, or pollute stored data.

#### Objective  
Implement a robust validator for `patient_name` in `validators.py` and enforce it within the appointment creation workflow. The validator must prevent dangerous input while remaining realistic and user-friendly.

#### Validation Rules
**To help you get started, this first challenge gives you the validation rules explicitly. However, future challenges will become progressively less explicit, requiring you to derive and justify appropriate validation choices on your own, just like a real security engineer.**

- Only letters, spaces, apostrophes, and hyphens allowed.
- Trim leading and trailing whitespace.
- Length: 2–50 characters after trimming.
- Reject:
  - SQL injection indicators
  - Angle brackets or script-like content
  - Unexpected punctuation sequences

#### Acceptance Criteria  
- Submitting a valid appointment with a legitimate name succeeds (`201`).
- Submitting malicious or malformed names is rejected (`400`) with a proper error message.
- Checker completes successfully and prints the flag.
