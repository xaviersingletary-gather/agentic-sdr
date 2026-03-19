# Agent 1: Researcher

**Version:** 2.0  
**Role:** Find companies, signals, and contacts in parallel  
**Model Tier:** Fast/Cheap (GPT-4o-mini or equivalent)  
**Frequency:** Weekly (Monday)

---

## Inputs

- ICP criteria:
  - Revenue: $500M+
  - Facilities: 11+
  - Geography: US/Canada
  - Industries: 3PL, Food & Beverage, Retail, Pharma, Manufacturing, CPG
- Exclusion list (from database)
- Clay API for company search

---

## Outputs

For each company found:

```json
{
  "company_name": "string",
  "domain": "string",
  "revenue_estimate": "number",
  "facility_count": "number",
  "industry": "string",
  "signals": [
    {
      "type": "job_post | news | earnings | leadership | expansion",
      "title": "string",
      "date": "YYYY-MM-DD",
      "source": "string",
      "recency_days": number
    }
  ],
  "contacts": [
    {
      "name": "string",
      "title": "string",
      "persona": "TDM | OCM | FS | ES"
    }
  ]
}
```

---

## Process

### Step 1: Check Deduplication Database

- Query `companies` table for domain processed in last 90 days
- If domain exists AND processed_date > (today - 90 days): **SKIP**

### Step 2: Call Clay API

- Run company search with ICP filters
- Get job posting signals (last 90 days)
- Get news signals (last 180 days)
- Get leadership changes (last 12 months)
- Find contacts (TDM, OCM names + titles)

### Step 3: Fallback - Exa API (earnings signals only)

- Search for earnings mentions of "OTIF", "chargebacks", "fulfillment failures"
- Add to signals if found

### Step 4: Rank by Signal Strength

- Sort output by: signal_recency + signal_count
- Return top 50 companies

---

## Deduplication Rules

- Before processing ANY company, check `companies` table
- If domain exists AND status != 'skipped': **SKIP**
- Write all new companies to database BEFORE outputting

---

## Error Handling

| Error | Action |
|-------|--------|
| Clay API returns 0 results | Log error + return empty list + notify human |
| Clay rate limited | Wait 60s + retry (max 3 retries) |
| Exa fails | Continue without earnings signals (not critical) |

---

## Database Write

Write to `companies` table:

| Field | Type | Notes |
|-------|------|-------|
| company_id | UUID | Primary key |
| name | TEXT | Company name |
| domain | TEXT UNIQUE | **Key for deduplication** |
| industry | TEXT | |
| revenue_estimate | TEXT | |
| facility_count | INTEGER | |
| signals_json | JSON | Store signals with dates |
| date_first_seen | DATE | |
| date_last_seen | DATE | |
| status | TEXT | new/in_progress/completed/skipped |

---

## API Calls

### Clay API

```
Endpoint: https://api.clay.com/v1/enrich/companies
Method: POST
Headers: Authorization: Bearer CLAY_API_KEY
```

### Exa API (fallback)

```
Endpoint: https://api.exa.ai/search
Method: POST
Headers: Authorization: Bearer EXA_API_KEY
```

---

## Success Criteria

- Return 50 companies (or as many as found)
- All have at least 1 signal
- Deduplication prevents reprocessing
