import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAY_API_KEY = os.getenv("CLAY_API_KEY", "")
EXA_API_KEY = os.getenv("EXA_API_KEY", "")
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY", "")
APOLLO_EMAIL_ACCOUNT_ID = os.getenv("APOLLO_EMAIL_ACCOUNT_ID", "")
HEYREACH_API_KEY = os.getenv("HEYREACH_API_KEY", "")
HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN", "")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_XAVIER_CHANNEL_ID = os.getenv("SLACK_XAVIER_CHANNEL_ID", "")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/sdr.db")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
DEDUP_DAYS = int(os.getenv("DEDUP_DAYS", "90"))
QUALITY_SCORE_NOTIFY_THRESHOLD = int(os.getenv("QUALITY_SCORE_NOTIFY_THRESHOLD", "70"))
QUALITY_SCORE_MIN_THRESHOLD = int(os.getenv("QUALITY_SCORE_MIN_THRESHOLD", "40"))
