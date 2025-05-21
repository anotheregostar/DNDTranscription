
import json
import pandas as pd
import sys
import os

def export_glossary_to_excel(glossary_path):
    with open(glossary_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    replace_section = data.get("Replace", {})
    ignore_list = data.get("Ignore", [])

    rows = []
    for campaign, entries in replace_section.items():
        for correct_word, variants in entries.items():
            row = {
                "Campaign": campaign,
                "Correct Term": correct_word
            }
            for i, variant in enumerate(variants):
                row[f"Variant {i+1}"] = variant
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel("glossary_config_wide.xlsx", index=False)
    print("✅ Exported glossary_config_wide.xlsx")

    with open("ignore_list.txt", "w", encoding="utf-8") as f:
        for word in sorted(set(ignore_list)):
            f.write(word + "\n")
    print("✅ Exported ignore_list.txt")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_glossary_to_excel.py glossary_config.json")
    else:
        export_glossary_to_excel(sys.argv[1])
