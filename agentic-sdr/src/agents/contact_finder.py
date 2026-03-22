from src.models.account import Account
from src.models.contact import Contact, PersonaType, OutreachStatus

SENIORITY_KEYWORDS = [
    "vp", "vice president", "director", "chief", "cfo", "coo", "ceo",
    "cto", "svp", "evp", "head of", "president", "general manager"
]

PERSONA_MAP = {
    PersonaType.tdm: [
        "warehouse", "distribution", "supply chain", "operations", "logistics",
        "fulfillment", "continuous improvement", "inventory", "facilities", "wms"
    ],
    PersonaType.financial_sponsor: [
        "cfo", "chief financial", "finance", "financial", "treasury", "controller"
    ],
    PersonaType.it: [
        "cto", "chief technology", "it director", "information technology",
        "systems", "technology", "infrastructure", "data"
    ],
    PersonaType.safety: [
        "safety", "ehs", "environmental health", "risk", "compliance"
    ],
    PersonaType.exec_sponsor: [
        "ceo", "chief executive", "president", "general manager", "managing director"
    ],
}

ICP_TITLE_QUERIES = [
    "VP Operations", "VP Supply Chain", "Director Warehouse",
    "Director Distribution", "Director Continuous Improvement",
    "Director Supply Chain", "CFO", "VP Finance", "Director Inventory",
    "Head of Operations", "COO"
]


def _is_director_plus(title: str) -> bool:
    title_lower = title.lower()
    return any(kw in title_lower for kw in SENIORITY_KEYWORDS)


def _classify_persona(title: str) -> PersonaType:
    title_lower = title.lower()
    for persona, keywords in PERSONA_MAP.items():
        if any(kw in title_lower for kw in keywords):
            return persona
    return PersonaType.odm


class ContactFinderAgent:
    def __init__(self, db, apollo_client):
        self.db = db
        self.apollo = apollo_client

    def find(self, account: Account) -> list[Contact]:
        raw_contacts = self.apollo.search_people(
            company_name=account.company_name,
            titles=ICP_TITLE_QUERIES
        )

        saved = []
        for raw in raw_contacts:
            title = raw.get("title", "")
            if not _is_director_plus(title):
                continue

            email = raw.get("email")
            if email and self.db.query(Contact).filter_by(email=email).first():
                continue

            persona = _classify_persona(title)
            contact = Contact(
                account_id=account.id,
                first_name=raw.get("first_name"),
                last_name=raw.get("last_name"),
                title=title,
                persona_type=persona,
                email=email,
                phone=raw.get("phone"),
                linkedin_url=raw.get("linkedin_url"),
                verified=bool(email),
                outreach_status=OutreachStatus.pending,
            )
            self.db.add(contact)
            saved.append(contact)

        self.db.commit()

        # Sort: TDM first, then Financial_Sponsor, then others
        priority = {PersonaType.tdm: 0, PersonaType.financial_sponsor: 1}
        saved.sort(key=lambda c: priority.get(c.persona_type, 99))

        return saved
