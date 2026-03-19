# Agent 7: Lead Magnet Creator

## Role Definition

| Attribute | Value |
|-----------|-------|
| **Name** | Lead Magnet Creator |
| **Type** | Content Agent |
| **Task** | Create the selected lead magnet asset |
| **Trigger** | After Account Strategist selects LEAD_MAGNET approach + Human #5 approval |
| **Position in Workflow** | Step 7 of 10 |

---

## Purpose

The Lead Magnet Creator builds the specific asset that will be used to engage the prospect. This could be an interactive ROI calculator, an industry benchmark report, or a relevant case study.

---

## Input

```
StrategyRecommendation:
- Company details
- Lead magnet type (ROI_CALCULATOR, BENCHMARK_REPORT, CASE_STUDY)
- Account data (revenue, facilities, industry, signals)
- Industry vertical
```

---

## Output

```
LeadMagnetAsset:
- Asset type
- Content/structure
- Input fields (for calculator)
- Data sources
- CTA
```

---

## Lead Magnet Types

### 1. ROI Calculator

**Purpose:** Interactive tool that calculates potential ROI based on prospect's specific data.

**Components:**
- Input fields (revenue, DCs, SKUs, current accuracy estimate)
- Calculation formula
- Peer benchmark comparisons
- CTA (schedule call)

**Example Input Fields:**
- Annual revenue ($)
- Number of distribution centers
- Average inventory value ($)
- Current accuracy estimate (%)
- Industry

**Example Output:**
- Estimated phantom inventory: $1.2M - $3.8M/year
- ROI timeline: 6 months
- Peer benchmark: 99.2% (top quartile)

---

### 2. Benchmark Report

**Purpose:** Industry-specific report showing how the prospect compares to peers.

**Components:**
- Industry overview
- Key metrics by quartile
- Best practices
- Methodology
- CTA (download + call)

**Sections:**
1. Executive Summary
2. Industry Benchmarks (inventory accuracy, OTIF, shrink)
3. Peer Comparisons
4. Key Findings
5. Recommendations
6. Methodology

---

### 3. Case Study

**Purpose:** Relevant success story from a similar company.

**Components:**
- Company profile (similar to prospect)
- Challenge
- Solution
- Results (quantified)
- CTA (talk to customer)

**Structure:**
- Title: "How [Similar Company] Achieved 99.9% Inventory Accuracy"
- Challenge: "Struggling with phantom inventory across X facilities"
- Solution: "Deployed autonomous drone scanning"
- Results: "$2.3M recovered in Year 1"

---

## Industry-Specific Customization

### For 3PLs

| Lead Magnet | Content |
|-------------|---------|
| ROI Calculator | "Calculate your contract value at 99.9% accuracy" |
| Benchmark Report | "3PL Inventory Accuracy Report" |
| Case Study | "How [similar 3PL] won higher-margin contracts" |

### For Food & Beverage

| Lead Magnet | Content |
|-------------|---------|
| ROI Calculator | "Calculate your shrink recovery" |
| Benchmark Report | "Food Distributor Inventory Accuracy Report" |
| Case Study | "How Gordon Food Services improved OTIF" |

### For Retail

| Lead Magnet | Content |
|-------------|---------|
| ROI Calculator | "Calculate your in-stock improvement" |
| Benchmark Report | "Retail Shrink & Availability Report" |
| Case Study | "How Target reduced chargebacks" |

### For Pharma

| Lead Magnet | Content |
|-------------|---------|
| ROI Calculator | "Calculate compliance risk reduction" |
| Benchmark Report | "Pharma Inventory Compliance Guide" |
| Case Study | "How [pharma co] achieved audit readiness" |

---

## Process

### Step 1: Select Template
Choose the appropriate template based on lead magnet type and industry

### Step 2: Customize Content
- Insert company-specific data (from research)
- Use company name throughout
- Reference specific signals found

### Step 3: Calculate Estimates
For ROI calculators:
- Use industry benchmarks to estimate ranges
- Show conservative and aggressive estimates

### Step 4: Add CTA
- Primary: Schedule a call
- Secondary: Download full report

---

## Example Output: ROI Calculator (Cheney Brothers)

```json
{
  "type": "ROI_CALCULATOR",
  "title": "Cheney Brothers: Inventory Opportunity Analysis",
  "inputs": [
    {
      "field": "annual_revenue",
      "label": "Annual Revenue",
      "value": "$3.2B",
      "editable": false
    },
    {
      "field": "facility_count",
      "label": "Distribution Centers",
      "value": "6+",
      "editable": false
    },
    {
      "field": "sku_count",
      "label": "SKUs",
      "value": "64,000+",
      "editable": false
    }
  ],
  "outputs": [
    {
      "metric": "Estimated Phantom Inventory",
      "range": "$1.2M - $3.8M/year",
      "assumption": "2-3% of inventory value"
    },
    {
      "metric": "Working Capital Recovery",
      "range": "$1.2M - $3.8M",
      "assumption": "At 99.9% accuracy"
    },
    {
      "metric": "Peer Benchmark",
      "value": "99.2% (Gordon Food Services)",
      "source": "Gather AI customer data"
    }
  ],
  "cta": {
    "primary": "Schedule 15-min call",
    "secondary": "Download Full Report"
  }
}
```

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Complete asset | 100% of requests |
| Company personalization | Every reference |
| Accurate calculations | Benchmarks verified |
| Clear CTA | Above fold |

---

## Tools Used

- Document creation
- Internal calculation logic
- Template system

---

## Next Agent

After completion, output goes to **Agent 8: Landing Page Agent** to build the personalized landing page.
