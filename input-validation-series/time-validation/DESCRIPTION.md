**Assignee:** You

**Priority:** High  

**Status:** To Do

**Deliverable:** Updated `validators.py`

**ETA:** End of day

#### Background  
The previous incremental challenge implemented appointment *date* validation. The next incremental task focuses on appointment *time* verification, another common and critical input validation surface: appointment times drive scheduling logic, calendar integrations, business hour enforcement, and downstream notifications. Accepting malformed or ambiguous times (e.g., "9:30 MM", "25:00", "12:60") can cause logic errors, missed appointments, and security/availability issues.

The current `appointment_api.py` accepts `appointment_time` without validation. You must add a robust validator for appointment times so the API only accepts clear, unambiguous, and business appropriate times.

#### Objective  
Implement a robust validator for `appointment_time` in `validators.py` and ensure it can be used by the appointment creation workflow.

#### Validation Rules
- Business hours enforcement:
  - Allowed times: `08:00` through `17:59` inclusive.
  - Reject times earlier than `08:00` and times `18:00` or later.

#### Acceptance Criteria  
- Submitting a valid appointment with a legitimate `appointment_time` succeeds (`201`).
- Submitting malformed or out-of-hours `appointment_time` is rejected (`400`) with a helpful error message.
- The checker completes successfully and prints the flag when the validator is in place and the API enforces it.
