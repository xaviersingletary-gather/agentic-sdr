# Agent 6: Follow-up Agent

**Version:** 2.0  
**Role:** Nurture contacts and book meetings  
**Model Tier:** Good Reasoning  
**Frequency:** Daily (runs every morning)

---

## Inputs

- Outreach log from Outreach Agent
- HubSpot contact responses (via API)
- HubSpot meeting link
- Enriched phone numbers

---

## Outputs

```json
{
  "meetings_booked": number,
  "replies_received": number,
  "follow_ups_sent": number,
  "moved_to_nurture": number,
  "details": [
    {
      "contact_name": "string",
      "action_taken": "meeting_booked | reply_received | follow_up_sent | moved_to_nurture",
      "channel": "linkedin | email | phone",
      "timestamp": "ISO date"
    }
  ]
}
```

---

## Query Logic

Find contacts where:

```sql
SELECT * FROM contacts 
WHERE sequence_status = 'active' 
AND next_action_date <= today;
```

---

## Sequence Logic

| Day | Condition | Action | Channel |
|-----|-----------|--------|---------|
| 3 | No response | "Did you see my message?" | LinkedIn |
| 7 | No response | "Quick question" | Email + Phone call |
| 14 | No response | "Last attempt" | Email |
| 30 | No response | Move to nurture | - |

---

## Response Handling

| Response | Action |
|----------|--------|
| "Interested" | Log → Notify human immediately (Slack) |
| "Meeting requested" | Log meeting → Update HubSpot stage |
| "Not now" | Log + pause 60 days |
| "Not interested" | Add to suppressions + log |
| "Unsubscribe" | Add to suppressions + never contact again |

---

## Phone Calls

- **ONLY** during business hours (9am-5pm)
- Max 10 calls per day
- Use enriched phone numbers
- Log outcome to follow_up_log

---

## Rate Limiting

| Limit | Value |
|-------|-------|
| Follow-ups per day | 30 |
| Phone calls per day | 10 |
| HARD STOP | After Day 14 (3 attempts max) |

---

## HubSpot Actions

### Meeting Booked

- Log "Meeting Scheduled" activity
- Update stage: "Lead" → "Meeting Booked"
- Notify human via Slack

### Reply Received

- Log "Reply Received"
- Tag contact with sentiment
- Notify human immediately

### Moved to Nurture (Day 30)

- Update lifecycle_stage: "lead" → "marketingqualifiedlead"
- Add to "Nurture" list
- sequence_status = 'nurturing'

---

## Database Write

Write to `follow_up_log` table:

| Field | Type |
|-------|------|
| follow_up_id | UUID (PK) |
| contact_id | UUID (FK) |
| sequence_day | INTEGER |
| channel | TEXT |
| message_copy | TEXT |
| response | TEXT |
| timestamp | TIMESTAMP |

Update `contacts` table:

| Field | Value |
|-------|-------|
| last_follow_up_date | today |
| follow_up_count | +1 |
| current_sequence_day | sequence_day |
| next_action_date | next sequence date |
| sequence_status | 'booked' / 'nurturing' / etc. |

---

## Update Suppressions (if needed)

If "not interested" or "unsubscribe":

```sql
INSERT INTO suppressions (email, reason, source, date_added)
VALUES (?, 'unsubscribe', 'follow_up_agent', CURRENT_DATE);
```

---

## Success Criteria

- All due contacts receive follow-up
- Meeting booked → immediate notification
- Reply received → immediate notification
- Opt-outs added to suppressions
- No contact touched more than 3 times