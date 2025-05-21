# 🎙️ WhisperX Transcription Automation Suite

A drag-and-drop audio transcription pipeline using [WhisperX](https://github.com/m-bain/whisperx), enriched with campaign mapping, timestamped TSVs, color-coded Excel files, spell-checking, glossary-based corrections, anomaly detection, and Markdown exports for Obsidian compatibility.

---

## 📦 Features

- **Drag and drop audio transcription** (.flac)
- Automatically renames files by campaign + speaker
- Uses **WhisperX** for precise transcription
- Outputs:
  - Individual `.tsv` files (timestamped speech)
  - A **color-coded Excel** master transcript
  - A clean **chat-style .txt** and **.md** transcript with YAML frontmatter
- **Glossary-based correction** and typo fixing
- **Anomaly detection** with suggestions
- Campaign/player configuration system
- Export/import glossary with Excel integration

---

## 🚀 Quick Start

### ✅ Requirements

- Windows
- [WhisperX](https://github.com/m-bain/whisperx) installed in a Conda environment
- Python (inside same Conda environment)
- HuggingFace token (optional, add to `batch_transcribe.bat`)

### 🏃‍♂️ How to Use

1. **Drag and drop** a folder of `.flac` files onto `1 - Create Transcripts.bat`
2. Sit back and wait — the script:
   - Renames files
   - Runs WhisperX
   - Applies glossary corrections
   - Outputs results in `/whisperx_output/`

---

## 🛠 Customization

### 🎭 Campaigns & Characters

Edit `config.json` to map filenames to speaker names for each campaign:

```json
{
  "campaigns": {
    "Waterdeep": {
      "dbuke": "Tinkler"
    },
    "Candlekeep": {
      "dbuke": "Lumpy"
    }
  },
  "whisperx_model": "large-v3"
}
```

💡 Filenames must match: `123-dbuke_0.flac` → "Tinkler"  
Add new campaigns or characters freely—just watch out for trailing commas!

### 🎨 Speaker Colors

Customize `combine_tsvs_with_colors.py` to change speaker color palette:

```python
SPEAKER_COLORS = [
  "FFFFCC", "CCFFCC", "CCE5FF", "FFCCCC", ...
]
```

### 📂 Output Directory

Default output: `[AudioFolder]/whisperx_output/`  
To change it: edit `output_root=` in the `.bat` script.

---

## ✨ Glossary System

### 📋 Edit Glossary

Edit terms in `glossary_config.json` directly or modify `glossary_config_wide.xlsx`.

- Replace section: maps incorrect → correct
- Ignore list: words skipped during spellchecking (e.g., D&D names)

Use these scripts:

- `export_glossary_to_excel.py glossary_config.json`
- `import_glossary_from_excel.py glossary_config_wide.xlsx ignore_list.txt`

### 📌 Anomalies & Suggestions

During processing, unknown or suspicious words are:

- Flagged and counted
- Suggestions stored in `glossary_suggestions.json`
- Logged in `anomalies_log.csv` (with count + proposed corrections)

---

## 🧠 Processing Pipeline

Full flow via `process_transcript.py`:

1. Combines lines by speaker
2. Applies glossary corrections
3. Detects unknown words
4. Suggests glossary additions
5. Exports:
   - ✅ `.xlsx` with corrections and color highlights
   - ✅ `.txt` and `.md` files with YAML headers
   - ✅ `anomalies_log.csv`
   - ✅ `glossary_suggestions.json`

---

## 🧼 Cleaner Sentences

To change how speech is grouped (by pause length):

Edit `convert_json_to_tsv.py` and update:

```python
MAX_PAUSE_SECONDS = 1.0
```

Try `0.8` for tighter grouping or `2.0` for looser grouping.

---

## 🧪 Troubleshooting

| Problem              | Solution                                                  |
|----------------------|-----------------------------------------------------------|
| WhisperX fails       | Check Conda env and HuggingFace token                     |
| Missing output       | Ensure filenames follow `###-handle_0.flac` format        |
| Jumbled transcript   | Fix speaker mappings in `config.json`                     |
| Permission errors    | Close files before running scripts                        |
| Bad transcription    | Update WhisperX or refine `MAX_PAUSE_SECONDS`             |

---

## 🧙 Obsidian-Ready Output

Final `.md` files are compatible with Obsidian and include:

- YAML frontmatter (Campaign, Session Date, Players)
- Auto-tag line (e.g., `#transcript #Waterdeep #session/2025-05-01`)

---

## 🧾 License & Credits

Built using [WhisperX](https://github.com/m-bain/whisperx).  
Local enhancements by Brian Buchanan & contributors.  
No license file included—assume personal/internal use only unless stated otherwise.

---

## 📣 Contributions

Feel free to fork, improve, or request features!

---
