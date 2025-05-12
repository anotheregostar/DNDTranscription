import sys
import os
import json
import re

input_folder = sys.argv[1]
campaign_name = sys.argv[2]

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

campaigns = config.get("campaigns", {})
mapping = campaigns.get(campaign_name, {})

pattern = re.compile(r"^\d+-([a-z0-9]+)_0\.flac$", re.IGNORECASE)

for filename in os.listdir(input_folder):
    match = pattern.match(filename)
    if match:
        original_key = match.group(1)
        new_name = mapping.get(original_key)
        if new_name:
            old_path = os.path.join(input_folder, filename)
            new_path = os.path.join(input_folder, f"{new_name}.flac")
            print(f"Renaming: {filename} -> {new_name}.flac")
            os.rename(old_path, new_path)
