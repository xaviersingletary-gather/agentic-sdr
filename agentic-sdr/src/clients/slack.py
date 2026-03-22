from slack_sdk import WebClient
from src.config import SLACK_BOT_TOKEN, SLACK_XAVIER_CHANNEL_ID


class SlackClient:
    def __init__(self):
        self.client = WebClient(token=SLACK_BOT_TOKEN)

    def notify_xavier(self, company_name: str, quality_score: float, signals: list[dict], hubspot_url: str = "") -> None:
        """Send a quality score notification to Xavier's personal channel."""
        signal_lines = "\n".join(f"  • {s['signal_type']} (+{s['points_contributed']}pts) — {s['signal_source']}" for s in signals)
        text = (
            f":dart: *High-Quality Account Detected*\n"
            f"*Company:* {company_name}\n"
            f"*Quality Score:* {quality_score}/100\n"
            f"*Signals:*\n{signal_lines}"
        )
        if hubspot_url:
            text += f"\n<{hubspot_url}|View in HubSpot>"

        self.client.chat_postMessage(channel=SLACK_XAVIER_CHANNEL_ID, text=text)
