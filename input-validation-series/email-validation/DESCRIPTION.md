**Assignee:** You

**Priority:** High  

**Status:** To Do

**Deliverable:** Updated `validators.py`

**ETA:** End of day

#### Background & Objective
This incremental challenge extends the appointment API work by focusing exclusively on *email validation*.

The current `appointment_api.py` accepts `patient_email` with no robust validation. The goal is to implement a robust validator that enforces a pragmatic, secure subset of email addresses suitable for web APIs.

#### Examples
- Valid email examples accepted:  
  - `user@example.com`
  - `firstname.lastname@company.co.uk`
  - `user+tag@sub.example.com`
  - `user@xn--d1acpjx3f.xn--p1ai` (punycode)
- Invalid examples rejected:
  - `notanemail` (missing `@`/domain)  
  - `@example.com` (missing local part)  
  - `user@localhost` (no TLD)  
  - `user..name@example.com` (consecutive dots)  
  - `user+<script>@example.com` (XSS-like)  
  - over 100 characters total

#### Acceptance Criteria
- Submitting a valid appointment with a valid email returns `201`.
- Submitting an appointment with an invalid email returns `400` with a clear error message that does not expose stack traces or internals.
- The provided checker completes successfully and prints the flag when all tests pass.
