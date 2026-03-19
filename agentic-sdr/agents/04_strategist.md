# Agent 4: Strategist

**Version:** 2.0  
**Role:** Create personalized outreach messages  
**Model Tier:** Best Creative (GPT-4o, Claude 3.5)  
**Frequency:** Wednesday (parallel with Enricher)

---

## Inputs

- Account signals from Qualifier
- Enriched contacts from Enricher
- Industry context (from MEMORY.md)

---

## Outputs

```json
{
  "company_name": "string",
  "contact_name": "string",
  "persona": "TDM | OCM | FS | ES",
  "linkedin_message_variants": [
    {
      "id": "A | B | C",
      "text": "string (under 150 words)",
      "signal_referenced": "string"
    }
  ],
  "email": {
    "subject": "string",
    "body": "string (under 200 words)"
  },
  "pain_point": "string",
  "meeting_ask": "string",
  "recommended_variant": "A | B | C"
}
```

---

## Personalization Rules

### TDM (Technical Decision Maker)

| Attribute | Value |
|-----------|-------|
| Titles | VP/Dir Warehouse Technology, Supply Chain Tech, WMS Manager |
| Language | Technical (WMS, inventory accuracy, digital twin, scan) |
| Pain points | Data-reality gap, cycle count labor, WMS optimization |
| Peer proof | Use other 3PLs or similar companies |

### OCM (Operational Decision Maker)

| Attribute | Value |
|-----------|-------|
| Titles | VP/Dir Distribution Operations, Fulfillment |
| Language | Operational (OTIF, chargebacks, throughput, labor) |
| Pain points | Fulfillment failures, retailer penalties, labor scarcity |
| Peer proof | Use same-industry examples |

### FS (Financial Sponsor)

| Attribute | Value |
|-----------|-------|
| Titles | CFO, VP Finance, SVP Supply Chain (P&L owner) |
| Language | ROI, working capital, safety stock |
| Pain points | Safety stock bloat, shrink, audit failures |
| Peer proof | Use ROI numbers |

### ES (Executive Sponsor)

| Attribute | Value |
|-----------|-------|
| Titles | COO, EVP Operations |
| Language | Strategic, competitive position |
| Pain points | Scale challenges, network visibility |

---

## Message Variant Selection

Generate 3 variants:

| Variant | Focus |
|---------|-------|
| A | Pain-focused |
| B | ROI-focused |
| C | Peer proof-focused |

**DEFAULT:** Recommend A (pain-focused) unless signal suggests otherwise

Human will select during checkpoint #2.

---

## Always Include

- 1-2 specific signal references (from signals input)
- HubSpot meeting link: `https://meetings.hubspot.com/[sales-rep-name]`
- CTA: 15-min call request

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No signals for company | Use generic industry pain point |
| No contact title | Use "operations leader" as fallback |
| Meeting link missing | **ERROR** - stop and alert human |

---

## Database Write

Write to `message_templates` table:

| Field | Type |
|-------|------|
| template_id | UUID (PK) |
| contact_id | UUID (FK) |
| linkedin_variant_a | TEXT |
| linkedin_variant_b | TEXT |
| linkedin_variant_c | TEXT |
| email_subject | TEXT |
| email_body | TEXT |
| selected_variant | CHAR(1) - null until human selects |
| approved | BOOLEAN - FALSE |
| created_date | DATE |

---

## Success Criteria

- 3 message variants per contact
- Messages under word limits
- Signal reference in every message
- Meeting link included
- Persona-appropriate language
