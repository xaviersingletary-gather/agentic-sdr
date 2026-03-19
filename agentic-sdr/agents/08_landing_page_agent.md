# Agent 8: Landing Page Agent

## Role Definition

| Attribute | Value |
|-----------|-------|
| **Name** | Landing Page Agent |
| **Type** | Creation Agent |
| **Task** | Build personalized landing page |
| **Trigger** | After Lead Magnet Creator + Human #6 approval |
| **Position in Workflow** | Step 8 of 10 |

---

## Purpose

The Landing Page Agent creates a personalized web page for each prospect that combines the lead magnet with company-specific research. This creates a tailored experience that demonstrates genuine understanding of the prospect's business.

---

## Input

```
LeadMagnetAsset:
- Asset type (calculator, report, case study)
- Content
- Company data

AccountData:
- Company name
- Revenue
- Facilities
- Industry
- Signals found
```

---

## Output

```
LandingPage:
- URL
- Content preview
- Screenshot
```

---

## Page Structure

### Header
```
┌─────────────────────────────────────────────────────────┐
│  [Gather AI Logo]                                      │
│                                                         │
│  Personalized for [Company Name]                        │
└─────────────────────────────────────────────────────────┘
```

### Hero Section
```
┌─────────────────────────────────────────────────────────┐
│  [Company Name]                                        │
│                                                         │
│  Inventory Opportunity Analysis                         │
│                                                         │
│  Based on your profile:                                │
│  • [Revenue] revenue                                   │
│  • [XX] distribution centers                          │
│  • [XX,XXX] SKUs                                      │
│  • [Industry]                                          │
└─────────────────────────────────────────────────────────┘
```

### Lead Magnet Section
```
┌─────────────────────────────────────────────────────────┐
│  YOUR CUSTOM [ASSET NAME]                              │
│                                                         │
│  [Interactive calculator OR Download button]            │
│                                                         │
│  [Live preview of outputs]                              │
└─────────────────────────────────────────────────────────┘
```

### Social Proof Section
```
┌─────────────────────────────────────────────────────────┐
│  HOW SIMILAR [INDUSTRY] COMPANIES STACK UP            │
│                                                         │
│  [Company A]: 99.4% accuracy                          │
│  [Company B]: 99.2% accuracy                          │
│  [Company C]: 98.8% accuracy                          │
│  Industry Average: 94.0%                                │
└─────────────────────────────────────────────────────────┘
```

### CTA Section
```
┌─────────────────────────────────────────────────────────┐
│  READY TO TALK?                                        │
│                                                         │
│  👤 [Contact Name], [Title]                            │
│  📅 15-min call to discuss your challenges             │
│                                                         │
│  [Schedule Time with Us]                               │
└─────────────────────────────────────────────────────────┘
```

### Footer
```
┌─────────────────────────────────────────────────────────┐
│  © 2024 Gather AI                                     │
│  Privacy | Terms                                       │
└─────────────────────────────────────────────────────────┘
```

---

## Personalization Elements

| Element | Source | Example |
|---------|--------|---------|
| Company name | Account data | "Cheney Brothers" |
| Revenue | Account data | "$3.2B" |
| Facilities | Account data | "6+ facilities" |
| SKUs | Signal research | "64,000+ SKUs" |
| Industry | Account data | "Food & Beverage" |
| Recent news | Signal research | "Florence, SC expansion" |
| Contact name | Contact data | "Cecil King, VP Operations" |
| Peer companies | Case studies | "Gordon Food Services" |

---

## Example: Cheney Brothers Landing Page

### URL
`gather.ai/cheney-brothers` or `gather.ai/p/cheney-brothers-inventory`

### Content

```
┌─────────────────────────────────────────────────────────┐
│  GATHER AI presents:                                    │
│  Inventory Opportunity Analysis for Cheney Brothers        │
│                                                         │
│  Based on your profile:                                │
│  • $3.2B revenue                                      │
│  • 64,000+ SKUs                                       │
│  • 6+ facilities (growing)                           │
│  • Multi-temp operations (frozen/refrigerated/dry) │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  YOUR CUSTOM ROI ESTIMATE                               │
│                                                         │
│  Phantom Inventory Recovery: $1.2M - $3.8M/year       │
│  (Based on 2-3% of inventory value)                    │
│                                                         │
│  Working Capital at 99.9% Accuracy: $1.2M - $3.8M     │
│                                                         │
│  [Calculate Your Numbers →]                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  SEE HOW SIMILAR FOOD DISTRIBUTORS STACK UP            │
│                                                         │
│  Gordon Food Services:  99.4% accuracy                 │
│  KeHE/DPI:           99.2% accuracy                    │
│  Industry Average:    94.0% accuracy                   │
│                                                         │
│  [Download Food Distributor Benchmark Report]          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  READY TO TALK?                                         │
│                                                         │
│  👤 Cecil King, VP Operations                           │
│  📅 15-min call to discuss your inventory challenges   │
│                                                         │
│  [Schedule Time with Cecil]                            │
└─────────────────────────────────────────────────────────┘
```

---

## Technical Implementation

### URL Structure
- Primary: `gather.ai/[company-name]`
- Alternative: `gather.ai/p/[unique-id]`

### Tracking
- UTM parameters for attribution
- Unique identifier for each page

### Form (if needed)
- Name
- Email
- Company
- Role (optional)

---

## Quality Checklist

| Item | Check |
|------|-------|
| Company name correct | ✅ |
| Revenue accurate | ✅ |
| Industry correct | ✅ |
| Signals referenced | ✅ |
| Contact name included | ✅ |
| CTA clear | ✅ |
| Mobile responsive | ✅ |
| Load time <3s | ✅ |

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Page created | 100% of requests |
| Personalization | All fields filled |
| Load time | <3 seconds |
| Mobile friendly | Yes |

---

## Tools Used

- Web creation tools
- Template system
- Analytics setup

---

## Next Agent

After completion, output goes to **Human Checkpoint #6** for review, then to **Agent 9: Outreach Agent** to send the landing page to prospects.
