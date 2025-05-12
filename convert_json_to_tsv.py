import sys
import json
import csv
import os
import re

# Settings
MAX_PAUSE_SECONDS = 1.0  # Max allowed gap between words before making a new sentence
# CORRECTIONS_FILE = "glossary_config.json"

# Load many-to-one corrections and invert to wrong → right map

# def load_corrections(path):
    # reverse_map = {}
    # if os.path.exists(path):
        # with open(path, "r", encoding="utf-8") as f:
            # data = json.load(f)
        # replace_section = data.get("Replace", {})
        # for correct, wrong_list in replace_section.items():
            # for wrong in wrong_list:
                # reverse_map[wrong.lower()] = correct
    # return reverse_map

# corrections = load_corrections(CORRECTIONS_FILE)

# # Function to apply corrections to a full sentence
# def apply_corrections(text, corrections):
    # def replacer(match):
        # word = match.group(0)
        # key = word.lower()
        # return corrections.get(key, word)
    # pattern = r'\b(' + '|'.join(re.escape(k) for k in corrections.keys()) + r')\b'
    # return re.sub(pattern, replacer, text, flags=re.IGNORECASE)

# Get JSON path from command line argument
json_path = sys.argv[1]

# Load JSON
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract all words from segments
words = []
for segment in data.get("segments", []):
    words.extend(segment.get("words", []))

# Get speaker name from filename
speaker_name = os.path.basename(json_path).split(".")[0]

# Output .tsv path
tsv_path = os.path.join(os.path.dirname(json_path), speaker_name + ".tsv")

# Group words into sentences
sentences = []
current = {"start": None, "end": None, "words": []}

for word in words:
    start = word.get("start", 0)
    end = word.get("end", 0)
    text = word.get("word", "").strip()

    if current["start"] is None:
        current["start"] = start
        current["end"] = end
        current["words"].append(text)
    elif (start - current["end"]) > MAX_PAUSE_SECONDS:
        sentences.append(current)
        current = {"start": start, "end": end, "words": [text]}
    else:
        current["end"] = end
        current["words"].append(text)

if current["words"]:
    sentences.append(current)

# Write TSV with corrections applied
with open(tsv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["Start", "End", "Speaker", "Text"])
    for sent in sentences:
        raw_text = " ".join(sent["words"])
        # corrected_text = apply_corrections(raw_text, corrections)
        writer.writerow([
            sent["start"],
            sent["end"],
            speaker_name,
            raw_text #corrected_text
        ])

print(f"✅ TSV created for {speaker_name}: {tsv_path}")



# import sys
# import json
# import csv
# import os

# # Settings
# MAX_PAUSE_SECONDS = 1.0  # Max allowed gap between words before making a new sentence

# # Get JSON path from command line argument
# json_path = sys.argv[1]

# # Load JSON
# with open(json_path, "r", encoding="utf-8") as f:
    # data = json.load(f)

# # Extract all words from segments
# words = []
# for segment in data.get("segments", []):
    # words.extend(segment.get("words", []))
    
# # Get speaker name from filename (e.g., "Jake.json" → "Jake")
# speaker_name = os.path.basename(json_path).split(".")[0]

# # # Create a folder for the speaker
# # output_folder = os.path.join(os.path.dirname(json_path), speaker_name)
# # os.makedirs(output_folder, exist_ok=True)

# # Output .tsv path inside the speaker's folder
# tsv_path = os.path.join(os.path.dirname(json_path), speaker_name + ".tsv")

# # tsv_path = os.path.join(output_folder, speaker_name + ".tsv")

# # # Output .tsv path
# # tsv_path = os.path.splitext(json_path)[0] + ".tsv"

# # Group words into sentences
# sentences = []
# current = {"start": None, "end": None, "words": []}

# for word in words:
    # start = word.get("start", 0)
    # end = word.get("end", 0)
    # text = word.get("word", "").strip()

    # if current["start"] is None:
        # current["start"] = start
        # current["end"] = end
        # current["words"].append(text)
    # elif (start - current["end"]) > MAX_PAUSE_SECONDS:
        # sentences.append(current)
        # current = {"start": start, "end": end, "words": [text]}
    # else:
        # current["end"] = end
        # current["words"].append(text)

# if current["words"]:
    # sentences.append(current)

# # Write TSV inside the speaker's folder
# with open(tsv_path, "w", newline="", encoding="utf-8") as f:
    # writer = csv.writer(f, delimiter="\t")
    # writer.writerow(["Start", "End", "Speaker", "Text"])
    # for sent in sentences:
        # writer.writerow([
            # sent["start"],
            # sent["end"],
            # speaker_name,
            # " ".join(sent["words"])
        # ])

# print(f"✅ TSV created for {speaker_name}: {tsv_path}")

#Old Code
# with open(tsv_path, "w", newline="", encoding="utf-8") as f:
    # writer = csv.writer(f, delimiter="\t")
    # writer.writerow(["Start", "End", "Speaker", "Text"])
    # for sent in sentences:
        # writer.writerow([
            # sent["start"],
            # sent["end"],
            # speaker_name,
            # " ".join(sent["words"])
        # ])

# print(f"✅ TSV created: {tsv_path}")
