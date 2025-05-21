import pandas as pd
import sys
import os
from collections import defaultdict

def import_glossary_from_excel(xlsx_path, ignore_txt=None):
    df = pd.read_excel(xlsx_path)
    glossary = {"Replace": defaultdict(dict), "Ignore": []}

    for _, row in df.iterrows():
        campaign = str(row["Campaign"]).strip()
        correct_term = str(row["Correct Term"]).strip()
        variants = []

        for col in row.index:
            if col.startswith("Variant") and pd.notna(row[col]):
                variants.append(str(row[col]).strip())

        glossary["Replace"][campaign][correct_term] = sorted(set(variants))

    if ignore_txt and os.path.exists(ignore_txt):
        with open(ignore_txt, "r", encoding="utf-8") as f:
            glossary["Ignore"] = sorted(set(line.strip() for line in f if line.strip()))

    # === Custom Write ===
    with open("glossary_config.json", "w", encoding="utf-8") as f:
        f.write("{\n")
        f.write('  "Replace": {\n')
        campaigns = list(glossary["Replace"].keys())
        for ci, campaign in enumerate(campaigns):
            f.write(f'    "{campaign}": {{\n')
            items = glossary["Replace"][campaign]
            keys = list(items.keys())
            for i, correct in enumerate(keys):
                variants = items[correct]
                variant_list = ", ".join(f'\"{v}\"' for v in variants)
                comma = "," if i < len(keys) - 1 else ""
                f.write(f'      "{correct}": [{variant_list}]{comma}\n')
            campaign_comma = "," if ci < len(campaigns) - 1 else ""
            f.write(f'    }}{campaign_comma}\n')
        f.write("  },\n")

        # Write Ignore list
        ignore_list = glossary["Ignore"]
        ignore_formatted = ", ".join(f'\"{w}\"' for w in ignore_list)
        f.write(f'  "Ignore": [{ignore_formatted}]\n')
        f.write("}\n")

    print("✅ glossary_config.json written in compact, readable format.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_glossary_from_excel.py glossary_config_wide.xlsx [ignore_list.txt]")
    else:
        xlsx = sys.argv[1]
        ignore_file = sys.argv[2] if len(sys.argv) > 2 else None
        import_glossary_from_excel(xlsx, ignore_file)

# import pandas as pd
# import json
# import sys
# import os
# from collections import defaultdict

# def import_glossary_from_excel(xlsx_path, ignore_txt=None):
    # df = pd.read_excel(xlsx_path)
    # glossary = {"Replace": defaultdict(dict), "Ignore": []}

    # for _, row in df.iterrows():
        # campaign = str(row["Campaign"]).strip()
        # correct_term = str(row["Correct Term"]).strip()
        # variants = []

        # for col in row.index:
            # if col.startswith("Variant") and pd.notna(row[col]):
                # variants.append(str(row[col]).strip())

        # if campaign not in glossary["Replace"]:
            # glossary["Replace"][campaign] = {}

        # glossary["Replace"][campaign][correct_term] = sorted(set(variants))

    # if ignore_txt and os.path.exists(ignore_txt):
        # with open(ignore_txt, "r", encoding="utf-8") as f:
            # glossary["Ignore"] = sorted(set(line.strip() for line in f if line.strip()))

    # with open("glossary_config.json", "w", encoding="utf-8") as f:
        # json.dump(glossary, f, indent=2, separators=(",", ": "), ensure_ascii=False)

    # print("✅ glossary_config.json has been updated.")

# if __name__ == "__main__":
    # if len(sys.argv) < 2:
        # print("Usage: python import_glossary_from_excel.py glossary_config_wide.xlsx [ignore_list.txt]")
    # else:
        # xlsx = sys.argv[1]
        # ignore_file = sys.argv[2] if len(sys.argv) > 2 else None
        # import_glossary_from_excel(xlsx, ignore_file)