# Agent 9: Outreach Agent

## Role Definition

| Attribute | Value |
|-----------|-------|
| **Name** | Outreach Agent |
| **Type** | Communication Agent |
| **Task** | Execute outreach sequence |
| **Trigger** | After Landing Page + Human #7 approval |
| **Position in Workflow** | Step 9 of 10 |

---

## Purpose

The Outreach Agent sends the personalized outreach messages to prospects, using the landing page as the core content. This agent handles multi-channel outreach (LinkedIn, Email, or both).

---

## Input

```
LandingPage:
- URL
- Content

EnrichedContacts:
- Company
- Contacts with emails and LinkedIn

StrategyRecommendation:
- Approach
- Sequence
- Channel
```

---

## Output

```
OutreachSent:
- Per contact:
  - Channel used
  - Message sent
  - Timestamp
- Confirmation of delivery
```

---

## Channels

### LinkedIn InMail

**Best for:** TDM, OCM (tech-savvy professionals)
**Length:** Short (2-3 sentences + landing page)
**Tone:** Professional, curious

**Template:**
```
Hi [Name],

Saw your role at [Company] — interesting scale ([X] facilities, [Y] employees).

I put together a quick analysis of where you might be leaving inventory on the table: [landingpageURL]

Curious if this resonates with what you're seeing?

Best,
[Your name]
```

### Email

**Best for:** FS, ES (executives), any channel
**Length:** Medium (3-4 paragraphs)
**Tone:** Professional, value-first

**Template:**
```
Subject: [Company] inventory opportunity

Hi [Name],

[Opening - reference something specific about company]

I analyzed [Company's] inventory operations and put together a personalized view of what accurate visibility could be worth: [landingpageURL]

Key findings:
- Estimated phantom inventory: $[X]M - $[Y]M/year
- Based on [Company's] scale of [X] facilities, [Y] SKUs
- Peer benchmark: [similar company] achieved 99.4% accuracy

Is this worth a 15-minute conversation?

Best,
[Your name]
```

### Multi-Channel

**Day 0:** LinkedIn connection + InMail
**Day 0:** Follow-up email
**Purpose:** Increase likelihood of engagement

---

## Message Customization

| Element | Source | Example |
|---------|--------|---------|
| Prospect name | Contact data | "Cecil" |
| Company name | Account data | "Cheney Brothers" |
| Specific stat | Signal research | "Your new Florence facility" |
| Peer reference | Case studies | "Gordon Food Services" |
| Landing page | Generated | "gather.ai/cheney-brothers" |

---

## Sequence Types

### Direct Sequence (3 touches)

| Day | Channel | Action |
|-----|---------|--------|
| 0 | LinkedIn + Email | Initial outreach with landing page |
| 3 | Email | "Did you see this?" |
| 7 | LinkedIn | Share relevant case study |

### Lead Magnet Sequence (5 touches)

| Day | Channel | Action |
|-----|---------|--------|
| 0 | LinkedIn + Email | Landing page |
| 3 | Email | "Did you see the calculator?" |
| 7 | LinkedIn | Share benchmark report |
| 14 | Email | "Is now a bad time?" |
| 30 | - | Move to nurture |

---

## Quality Checklist

| Item | Check |
|------|-------|
| Correct name spelling | ✅ |
| Correct company name | ✅ |
| Personalized content | ✅ |
| Landing page link works | ✅ |
| CTA clear | ✅ |
| No grammar errors | ✅ |
| Appropriate tone | ✅ |

---

## Example: Cheney Brothers Outreach

### LinkedIn Message (Day 0)

```
Hi Cecil,

Congrats on the new Florence facility — 386,000 sq ft is significant expansion.

With 64,000+ SKUs across frozen, refrigerated, and dry, I'm guessing inventory visibility across your network is top of mind.

I put together a quick analysis of where you might be leaving money on the table: gather.ai/cheney-brothers

Curious if this resonates with what you're seeing?

Best,
[Your name]
```

### Email (Day 0)

```
Subject: Cheney Brothers inventory opportunity

Hi Cecil,

I analyzed Cheney Brothers' inventory operations and put together a personalized view of what accurate visibility could be worth.

Key findings:
- Estimated phantom inventory: $1.2M - $3.8M/year
- Based on your scale: 6+ facilities, 64,000+ SKUs
- Peer benchmark: Gordon Food Services achieved 99.4% accuracy

See where you stack up: gather.ai/cheney-brothers

Is this worth a 15-minute conversation?

Best,
[Your name]
```

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Messages sent | 100% of contacts |
| Delivery rate | >95% |
| Personalization | 100% fields |
| No errors | 100% |

---

## Tools Used

- `message` - Send messages
- `browser` - LinkedIn outreach
- Email system (if integrated)

---

## Next Agent

After completion, output goes to **Human Checkpoint #7** for review, then to **Agent 10: Follow-up Agent** for nurturing.
