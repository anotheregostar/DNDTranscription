import sys
import json
import os

folder_name = sys.argv[1]

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

campaigns = config.get("campaigns", {})

# Find matching campaign
matched_campaign = None
for campaign in campaigns:
    if campaign.lower() in folder_name.lower():
        matched_campaign = campaign
        break

if not matched_campaign:
    print("NO_MATCH")
else:
    print(matched_campaign)
