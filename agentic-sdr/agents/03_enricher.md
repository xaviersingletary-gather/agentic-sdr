# Agent 3: Enricher

**Version:** 2.0  
**Role:** Get contact details for approved accounts  
**Model Tier:** Fast + API Access  
**Frequency:** Weekly (Wednesday) - parallel with Strategist

---

## Inputs

- Approved accounts from Human #1 (top 10)
- Contact names from Researcher

---

## Outputs

```json
{
  "company_name": "string",
  "contact_name": "string",
  "title": "string",
  "persona": "TDM | OCM | FS | ES",
  "email": "string or null",
  "email_verified": boolean,
  "phone": "string or null",
  "phone_type": "direct | mobile | main | null",
  "linkedin_url": "string or null"
}
```

**Summary:**

```json
{
  "total_contacts": number,
  "email_found": number,
  "phone_found": number,
  "fully_enriched": number,
  "failed": number
}
```

---

## Primary Source: Clay API

- Clay's internal waterfall: tries multiple sources until verified email found
- Returns: email (verified), phone, LinkedIn URL

---

## Validation Rules

| Field | Rule |
|-------|------|
| Email | Must be verified (Clay marks verified/unverified) |
| Phone | Prefer direct dials over main company numbers |
| No email found | Mark as "manual_research_needed" |

---

## Suppression Check (MANDATORY)

- Before ANY enrichment, check `suppressions` table
- If email in suppressions: **SKIP entirely**
- Log to follow_up_log with reason

```sql
SELECT * FROM suppressions WHERE email = ?;
```

---

## Rate Limiting

- Implement 36ms delay between requests
- If rate limited: Wait 60s + retry (max 2 retries)

---

## Database Write

Write to `contacts` table:

| Field | Type | Default |
|-------|------|---------|
| contact_id | UUID | Primary key |
| company_id | UUID | FK to companies |
| name | TEXT | NOT NULL |
| title | TEXT | |
| persona | TEXT | |
| email | TEXT | |
| email_verified | BOOLEAN | FALSE |
| phone | TEXT | |
| phone_type | TEXT | |
| linkedin_url | TEXT | |
| hubspot_contact_id | TEXT | null |
| current_sequence_day | INTEGER | 0 |
| next_action_date | DATE | null |
| sequence_status | TEXT | 'new' |

---

## Update Companies

- If 1+ contacts enriched: status = "enriched"
- If all failed: status = "enrichment_failed"

---

## Success Criteria

- Enrich at least 80% of contacts
- All enriched contacts have verified emails
- Suppression check runs before any action
