# Agent 5: Outreach Agent

**Version:** 2.0  
**Role:** Execute multi-channel outreach and log to HubSpot  
**Model Tier:** Reliable + API Capable  
**Frequency:** Weekly (Friday)

---

## Inputs

- Approved message templates from Human #2
- Enriched contacts with emails/phones
- HubSpot meeting link
- HubSpot API key
- HeyReach API key + campaign ID
- Instantly/Smartlead API key (email)

---

## Outputs

```json
{
  "sent_count": number,
  "failed_count": number,
  "details": [
    {
      "contact_name": "string",
      "company_name": "string",
      "channel": "linkedin | email",
      "status": "sent | failed",
      "timestamp": "ISO date",
      "hubspot_contact_id": "string or null",
      "heyreach_message_id": "string or null"
    }
  ]
}
```

---

## Send Sequence

### Step 1: HeyReach API → LinkedIn (morning)

```
POST https://api.heyreach.io/api/v1/connection/request
Headers: Authorization: Bearer HEYREACH_API_KEY
Body: {
  "profile_url": linkedin_url,
  "message": message_text,
  "campaign_id": HEYREACH_CAMPAIGN_ID
}
```

Store `heyreach_message_id` in outreach_log.

### Step 2: Email via Instantly/Smartlead (afternoon, 4 hours later)

```
POST https://api.instantly.ai/api/v1/campaigns/send
Headers: Authorization: Bearer INSTANTLY_API_KEY
Body: {
  "to": email,
  "subject": subject_line,
  "body": email_body,
  "meeting_link": hubspot_meeting_url
}
```

---

## Suppression Check (MANDATORY)

Before sending ANY message:

```sql
SELECT * FROM suppressions WHERE email = ?;
```

- If email in suppressions: **SKIP + log warning**
- If contact has sequence_status = 'opted_out': **SKIP**

---

## Rate Limiting (CRITICAL)

| Channel | Limit |
|---------|-------|
| HeyReach | Max 30 connection requests/day (enforced by HeyReach) |
| Email | Max 100/day |
| **HARD STOP** | No sends after 5pm local time |

- 20-minute delay between channels

---

## HubSpot Logging

For each contact:

1. **CREATE/UPDATE CONTACT**
   - Fields: name, email, company, phone, persona
   - List: "SDR Outbound"

2. **LOG OUTREACH ACTIVITY**
   - Activity type: "Outreach Sent"
   - Include: message copy, channel, timestamp

3. **SET PROPERTIES**
   - lifecycle_stage: "lead"
   - hs_lead_status: "Attempted to Contact"
   - next_follow_up: (today + 3 days)

---

## Database Write

Write to `outreach_log` table:

| Field | Type |
|-------|------|
| outreach_id | UUID (PK) |
| contact_id | UUID (FK) |
| company_id | UUID (FK) |
| channel | TEXT |
| sequence_day | INTEGER = 0 |
| message_copy | TEXT (truncated) |
| sent_timestamp | TIMESTAMP |
| hubspot_activity_id | TEXT |
| heyreach_message_id | TEXT |
| status | TEXT |

Update `contacts` table:

| Field | Value |
|-------|-------|
| last_outreach_date | today |
| outreach_count | +1 |
| current_sequence_day | 0 |
| next_action_date | today + 3 days |
| sequence_status | 'active' |

---

## Error Handling

| Error | Action |
|-------|--------|
| LinkedIn rate limited | Skip LinkedIn, do email only, log warning |
| Email bounce | Mark as "bounced" in HubSpot, skip follow-up |
| HubSpot API down | Queue messages, retry on next run |
| Invalid email | Mark as "invalid", do not retry |

---

## Success Criteria

- All approved contacts receive outreach
- HubSpot contact created for each
- Activity logged in HubSpot
- HeyReach message ID captured
- Zero suppressions violated
