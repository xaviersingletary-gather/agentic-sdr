# Human Review Templates

Templates for each human-in-the-loop checkpoint in the agentic SDR workflow.

---

## Checkpoint #1: After Prospecting

**Reviewer:** Human
**Task:** Approve new lead list from Prospector

### Review Checklist

- [ ] Quality of candidates (ICP alignment)
- [ ] No duplicates with exclusion list
- [ ] Sufficient quantity (20-100 accounts)
- [ ] Basic firmographics present

### Decision

| Option | Action |
|--------|--------|
| ✅ Approve | Proceed to ICP Qualifier |
| ❌ Reject | Return to Prospector with feedback |
| ⚠️ Partial | Approve subset, reject rest |

### Notes Template

```
REVIEW #1 - [Date]

Accounts Reviewed: [X]
Approved: [X]
Rejected: [X]

Key Feedback:
-

Next Step: [Proceed to ICP Qualifier]
```

---

## Checkpoint #2: After ICP Scoring

**Reviewer:** Human
**Task:** Approve HIGH-fit accounts

### Review Checklist

- [ ] ICP scoring accurate
- [ ] HIGH-fit accounts genuinely qualify
- [ ] LOW/OUT accounts correctly scored
- [ ] Reason for scoring valid

### Decision

| Option | Action |
|--------|--------|
| ✅ Approve all | Proceed to Signal Hunter |
| ✅ Approve subset | Proceed with HIGH only |
| ❌ Reject all | Return to ICP Qualifier |

### Notes Template

```
REVIEW #2 - [Date]

HIGH Accounts: [X]
MEDIUM Accounts: [X]
LOW Accounts: [X]

Key Feedback:
-

Next Step: [Proceed to Signal Hunter for HIGH accounts]
```

---

## Checkpoint #3: After Signal Detection

**Reviewer:** Human
**Task:** Approve accounts with strong signals

### Review Checklist

- [ ] Signals accurately identified
- [ ] Signal strength appropriately scored
- [ ] Evidence cited for each signal
- [ ] Accounts without signals flagged for nurture

### Decision

| Option | Action |
|--------|--------|
| ✅ Approve | Proceed to Contact Discovery |
| ⚠️ Re-signal | Return for additional research |
| ❌ Reject | Mark as no-go |

### Notes Template

```
REVIEW #3 - [Date]

STRONG Signals: [X]
MEDIUM Signals: [X]
WEAK/None: [X]

Key Feedback:
-

Next Step: [Proceed to Contact Finder for STRONG accounts]
```

---

## Checkpoint #4: After Contact Discovery

**Reviewer:** Human
**Task:** Verify contact accuracy

### Review Checklist

- [ ] Correct names found
- [ ] Titles match persona
- [ ] At least TDM + OCM identified
- [ ] LinkedIn URLs verified

### Decision

| Option | Action |
|--------|--------|
| ✅ Approve | Proceed to Account Strategist |
| ❌ Fix contacts | Return for corrections |
| ⚠️ Partial | Proceed with verified only |

### Notes Template

```
REVIEW #4 - [Date]

Accounts with TDM: [X]/[X]
Accounts with 2+ personas: [X]/[X]

Contacts Requiring Fix:
-

Next Step: [Proceed to Account Strategist]
```

---

## Checkpoint #5: After Strategy

**Reviewer:** Human
**Task:** Approve outreach approach

### Review Checklist

- [ ] Approach (Direct vs Lead Magnet) justified
- [ ] Lead magnet type appropriate
- [ ] Channel selection logical
- [ ] Persona priority correct

### Decision

| Option | Action |
|--------|--------|
| ✅ Approve | Execute strategy |
| ❌ Change approach | Return to Account Strategist |

### Notes Template

```
REVIEW #5 - [Date]

Approach Approved: [Direct/Lead Magnet]
Lead Magnet: [Type]
Channel: [LinkedIn/Email/Multi]

Key Feedback:
-

Next Step: [Execute]
```

---

## Checkpoint #6: Before Landing Page

**Reviewer:** Human
**Task:** Review personalized content

### Review Checklist

- [ ] Company name correct
- [ ] Revenue/facilities accurate
- [ ] Signals referenced
- [ ] CTA appropriate
- [ ] Brand consistency

### Decision

| Option | Action |
|--------|--------|
| ✅ Approve | Publish landing page |
| ❌ Fix | Return for corrections |

### Notes Template

```
REVIEW #6 - [Date]

Landing Page: [URL]
Company: [Name]

Corrections Needed:
-

Next Step: [Publish]
```

---

## Checkpoint #7: Before Outreach

**Reviewer:** Human
**Task:** Approve final message

### Review Checklist

- [ ] Personalization correct
- [ ] No grammar/spelling errors
- [ ] Tone appropriate
- [ ] Landing page link works
- [ ] CTA clear

### Decision

| Option | Action |
|--------|--------|
| ✅ Approve | Send outreach |
| ❌ Edit message | Return for edits |

### Notes Template

```
REVIEW #7 - [Date]

Contacts: [X]
Channel: [LinkedIn/Email/Both]

Message Approved: [Yes/No]
Edits Required:
-

Next Step: [Send]
```

---

## Checkpoint #8: After Follow-up

**Reviewer:** Human
**Task:** Review results and hand off

### Review Checklist

- [ ] Meeting booked details correct
- [ ] All context passed to sales
- [ ] Nurture list populated
- [ ] Metrics recorded

### Decision

| Option | Action |
|--------|--------|
| ✅ Hand off | Sales takes over |
| ⚠️ Further nurture | Keep in workflow |

### Notes Template

```
REVIEW #8 - [Date]

Meetings Booked: [X]
Moved to Nurture: [X]

Handed Off To: [Sales Rep]
Account Notes:
-

Workflow Complete
```