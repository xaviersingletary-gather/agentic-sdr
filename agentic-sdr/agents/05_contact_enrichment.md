# Agent 5: Contact Enrichment

## Role Definition

| Attribute | Value |
|-----------|-------|
| **Name** | Contact Enrichment |
| **Type** | Data Agent |
| **Task** | Get contact details for buying committee |
| **Trigger** | After Contact Finder |
| **Position in Workflow** | Step 5 of 10 |

---

## Purpose

The Contact Enrichment agent takes the names and titles from the Contact Finder and enriches them with contact information: email addresses, phone numbers, and verified LinkedIn profiles.

---

## Input

```
BuyingCommittee per account:
- Company details
- List of contacts:
  - Name
  - Title
  - Persona type
  - LinkedIn URL (if available)
```

---

## Output

```
EnrichedContacts per account:
- Company details
- Full contacts with:
  - Name
  - Title
  - Persona
  - Email
  - Phone (optional)
  - LinkedIn URL
  - Confidence score
```

---

## Enrichment Data Points

| Field | Required? | Source |
|-------|-----------|--------|
| Email | Yes | Apollo, ZoomInfo, LinkedIn Sales Nav |
| Phone | No | ZoomInfo, Apollo |
| LinkedIn URL | Yes | From Contact Finder + verification |
| Confidence | Auto | Calculated based on source quality |

---

## Confidence Scoring

| Source | Confidence |
|--------|------------|
| Verified email (Apollo/ZoomInfo) | HIGH |
| LinkedIn Sales Nav | HIGH |
| Direct from company website | MEDIUM |
| Inferred from pattern | LOW |

---

## Process

### Step 1: Validate LinkedIn
For each contact:
- Verify LinkedIn URL is correct
- Check profile is current (recent activity)

### Step 2: Find Email
Search for:
- Work email pattern (@company.com)
- Corporate directory
- Email finding tools

### Step 3: Find Phone
If available from:
- ZoomInfo
- Apollo
- Company website

### Step 4: Score Confidence
Assign confidence level based on source quality

---

## Email Patterns

| Company Domain Pattern | Example |
|---------------------|---------|
| firstname.lastname@company.com | cecil.king@cheneybrothers.com |
| firstname@company.com | cecil@cheneybrothers.com |
| lastname.firstname@company.com | king.cecil@cheneybrothers.com |
| firstinitiallastname@company.com | cking@cheneybrothers.com |

---

## Example Output

```json
{
  "company": {
    "name": "Cheney Brothers",
    "domain": "cheneybrothers.com"
  },
  "contacts": [
    {
      "name": "Cecil King",
      "title": "VP Operations",
      "persona": "TDM",
      "email": "cecil.king@cheneybrothers.com",
      "phone": "+1-555-123-4567",
      "linkedin_url": "https://linkedin.com/in/cecil-king-68162128",
      "confidence": "HIGH"
    },
    {
      "name": "Peter Borradaile",
      "title": "Director of Operations",
      "persona": "OCM",
      "email": "peter.borradaile@cheneybrothers.com",
      "phone": "",
      "linkedin_url": "https://linkedin.com/in/peter-borradaile",
      "confidence": "MEDIUM"
    }
  ]
}
```

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| No email found | Flag as "email needed" - use LinkedIn outreach |
| Email bounces | Mark as invalid, try alternative pattern |
| Contact no longer at company | Note as "stale", flag for re-research |

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Emails found | >70% of contacts |
| High confidence | >50% of emails |
| Phone numbers | >30% of contacts |

---

## Tools Used

- `web_search` - Find email patterns
- Apollo (if available)
- ZoomInfo (if available)
- LinkedIn Sales Navigator (if available)

---

## Next Agent

After completion, output goes to **Human Checkpoint #4** for review, then to **Agent 6: Account Strategist**.
