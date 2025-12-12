**Assignee:** You

**Priority:** High  

**Status:** To Do

**Deliverable:** Updated `validators.py`

**ETA:** End of day

#### Background  
This next challenge focuses on *appointment date validation*, which represents a common real world attack surface where malformed or adversarial dates can cause logic errors, scheduling confusion, or downstream parsing/authorization issues.

The current `appointment_api.py` accepts `appointment_date` with no validation, allowing inputs that could break scheduling logic or bypass business rules.

#### Objective  
Implement a robust validator for `appointment_date` in `validators.py` and (when integrated into the API) enforce it within the appointment creation workflow. The validator must be conservative, production-ready, and clear to users when their input is invalid.

#### Validation Rules
- Input must be a string in strict ISO date format: `YYYY-MM-DD`.

#### Acceptance Criteria  
- Submitting a valid appointment with a legitimate future date within 90 days succeeds (`201`).  
- The provided `checker` verifies the validator behavior and prints the flag when all tests pass.
