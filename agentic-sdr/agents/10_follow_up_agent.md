# Agent 10: Follow-up Agent

## Role Definition

| Attribute | Value |
|-----------|-------|
| **Name** | Follow-up Agent |
| **Type** | Nurture Agent |
| **Task** | Nurture and follow-up to book meetings |
| **Trigger** | After Outreach Agent + Human #7 approval |
| **Position in Workflow** | Step 10 of 10 |

---

## Purpose

The Follow-up Agent manages the post-outreach phase: sending follow-up messages, tracking responses, and either booking a meeting or moving the prospect to a nurture track.

---

## Input

```
OutreachSent:
- Per contact:
  - Channel used
  - Message sent
  - Timestamp

Response data:
- Opens/clicks (if tracked)
- Replies received
```

---

## Output

```
Result per contact:
- Meeting booked: Yes/No
- If Yes: Meeting details
- If No: Move to nurture track
- Next action
```

---

## Follow-up Schedule

### Responsive Track (Replied)

| Scenario | Action |
|----------|--------|
| Positive reply | Book meeting immediately |
| Question asked | Answer + propose call |
| Want more info | Send relevant content |

### Unresponsive Track (No reply)

| Day | Action | Channel |
|-----|--------|---------|
| 0 | Initial outreach sent | LinkedIn + Email |
| 3 | Soft follow-up | Email |
| 7 | Share case study | LinkedIn |
| 14 | Final attempt | Email |
| 30 | Move to nurture | Internal |

---

## Follow-up Messages

### Day 3: Soft Follow-up

**Email:**
```
Subject: Following up on [Company] inventory

Hi [Name],

Just wanted to bump this to the top of your inbox.

The landing page has a calculator that might be useful: [landingpageURL]

No pressure — happy to chat whenever makes sense.

Best,
[Your name]
```

**LinkedIn:**
```
Hey [Name], just following up. Let me know if this isn't relevant to your current priorities.
```

---

### Day 7: Share Case Study

**LinkedIn:**
```
[Name], saw that [similar company] just achieved 99.4% inventory accuracy — thought you might find this interesting given your scale at [Company].

Full story: [link]

Curious if this is on your radar?
```

---

### Day 14: Final Attempt

**Email:**
```
Subject: Quick question

Hi [Name],

I know you're busy. Just wanted to make one last touchpoint.

Is now a bad time to discuss [Company's] inventory visibility? Or is this something your team is looking into?

Either way — I'll bow out after this.

Best,
[Your name]
```

---

## Meeting Booking

### When Prospect Says Yes

1. **Confirm interest:** "Great, would you have 15 minutes this week?"
2. **Propose times:** Offer 2-3 specific slots
3. **Send invite:** Calendar invite with Gather AI details
4. **Notify sales:** Alert human for handoff

### Meeting Confirmation Template

```
Subject: Confirmed: Inventory Discussion with Gather AI

Hi [Name],

Looking forward to chatting!

Date: [Day, Date]
Time: [Time] ET
Duration: 15 minutes

Zoom link: [link]

I'll send a calendar invite shortly.

Best,
[Your name]
```

---

## Handoff to Sales

When meeting is booked:

```
┌─────────────────────────────────────────────────────────┐
│  MEETING BOOKED - HANDOFF TO SALES                     │
│                                                         │
│  Company: [Name]                                        │
│  Contact: [Name], [Title]                              │
│  Meeting: [Date] at [Time]                             │
│  Account Strategy: [Direct/Lead Magnet]                │
│  Key Pain Points: [List]                               │
│  Signals Found: [List]                                 │
│                                                         │
│  Notes: [Any relevant context]                         │
└─────────────────────────────────────────────────────────┘
```

---

## Nurture Track

When no response after Day 14:

1. **Move to nurture list** in CRM
2. **Set reminder** for 90 days
3. **Add to newsletter** (if applicable)
4. **Monitor for new signals** (re-trigger if signals emerge)

### Nurture Re-entry Criteria

| Trigger | Action |
|---------|--------|
| New DC announced | Re-engage with new landing page |
| Hiring for CI/Inventory | Send relevant case study |
| WMS change announced | Reach out about integration |

---

## Metrics Tracked

| Metric | Definition |
|--------|------------|
| Response rate | % of prospects who replied |
| Meeting booking rate | % of outreach → meetings |
| Days to response | Average time to first reply |
| Touches per booked meeting | Average outreach attempts |

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Follow-ups sent | 100% of unresponsive |
| Response rate | >30% |
| Meeting booking rate | >15% |
| Average days to meeting | <21 |

---

## Tools Used

- `message` - Send follow-ups
- `web_search` - Monitor for new signals
- CRM integration (if available)

---

## End of Workflow

After Follow-up Agent completes:
- **Meeting booked:** Human Checkpoint #8 → Handoff to sales
- **Nurture:** Added to nurture list, workflow ends