import os
from datetime import datetime, timedelta

import pandas as pd
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

REMINDER_DAYS = 0 # testing

slack = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

# Load schedule
df = pd.read_csv("schedule.csv")
df["Date"] = pd.to_datetime(df["Date"]).dt.date

today = datetime.utcnow().date()
target_date = today + timedelta(days=REMINDER_DAYS)

upcoming = df[df["Date"] == target_date]

for _, row in upcoming.iterrows():
    message = (
        f"👋 Hi {row['Speaker']}!\n\n"
        f"Just a reminder that you’re scheduled to present at Mechanics Journal Club"
        f"on *{row['Date']}* (in {REMINDER_DAYS} days).\n\n"
        f"📄 Please suggest 3 papers that that everyone can vote for, and presented the most voted option. \n\n"
        f"Thanks!"
    )

    try:
        slack.chat_postMessage(
            channel=row["SlackID"],
            text=message
        )
        print(f"Sent reminder to {row['Speaker']}")

    except SlackApiError as e:
        print(f"Failed to message {row['Speaker']}: {e.response['error']}")
