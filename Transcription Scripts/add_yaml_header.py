import os
import sys
import re
from datetime import datetime

def extract_metadata_from_filename(filename):
    match = re.match(r"(.*)\s(\d{4}-\d{2}-\d{2})", filename)
    if not match:
        raise ValueError("Filename must include campaign and date in format: 'Campaign YYYY-MM-DD'")
    campaign = match.group(1).strip()
    session_date = match.group(2)
    return campaign, session_date

def extract_players_from_content(content):
    match = re.search(r"Session Attendance:\n(.*?)\n\n", content, re.DOTALL)
    if match:
        players_raw = match.group(1)
        players = [line.strip() for line in players_raw.splitlines() if line.strip()]
        return players
    return []

def apply_yaml_header(file_path):
    base_filename = os.path.basename(file_path)
    campaign, session_date = extract_metadata_from_filename(base_filename.replace('_transcript_corrected.txt', ''))

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    players = extract_players_from_content(content)

    yaml_block = "---\n"
    yaml_block += "Type: Transcript\n"
    yaml_block += f"Campaign: \"{campaign}\"\n"
    yaml_block += f"Session Date: \"{session_date}\"\n"
    yaml_block += "Players:\n"
    for player in players:
        yaml_block += f"  - {player}\n"
    yaml_block += "---\n\n"

    tag_line = f"#transcript #{campaign} #session/{session_date} #players/" + "_".join(players) + "\n"

    full_text = yaml_block + content.strip() + "\n\n" + tag_line

    new_txt_filename = f"{campaign} {session_date} Final Transcript.txt"
    new_md_filename = f"{campaign} {session_date} Final Transcript.md"

    new_txt_path = os.path.join(os.path.dirname(file_path), new_txt_filename)
    new_md_path = os.path.join(os.path.dirname(file_path), new_md_filename)

    with open(new_txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    with open(new_md_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ YAML header (minimal) + Obsidian tags added and files saved as:\n  - {new_txt_path}\n  - {new_md_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python add_yaml_header.py <transcript_file>")
        sys.exit(1)

    transcript_file = sys.argv[1]
    apply_yaml_header(transcript_file)
