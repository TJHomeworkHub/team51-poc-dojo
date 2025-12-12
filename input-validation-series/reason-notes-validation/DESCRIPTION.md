**Assignee:** You

**Priority:** High  

**Status:** To Do

**Deliverable:** Updated `validators.py`

**ETA:** End of day

#### Background  
Reason and notes fields are free text inputs that often carry clinical context, triage details, and freeform clinician/patient commentary. Left unvalidated they can be a source of XSS, SQL-injection-looking payloads, or overly long/malformed content that breaks downstream systems (notifications, storage, analytics).

#### Objective  
Implement robust alidators for `reason` and `notes` in `validators.py` and make them available for the appointment creation workflow.

#### Validation Rules
- **Reason**
  - Length: 10-200 characters after trimming.
- **Notes**
  - Length: 0-500 characters when provided.

#### Acceptance Criteria  
- Creating an appointment with valid `reason` and optionally valid `notes` succeeds (`201`).
- Submitting invalid or malicious `reason` or `notes` is rejected (`400`) with a clear error message.
- The checker should complete successfully and print the flag when the validators are implemented and enforced.
