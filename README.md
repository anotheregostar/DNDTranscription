#### **Description**
This system lets you **drag and drop** a folder full of .flac files and automatically:

- Rename audio files based on Campaign + Speaker
- Transcribe using WhisperX
- Create individual .tsv files (timestamped speech chunks)
- Combine into:
	- A **color-coded Excel** transcript
	- A **plain Text** version

All output goes to a neat `/whisperx_output/` folder.

---
#### **Quick Start**

##### **1. Requirements**

- Windows
- WhisperX installed inside a Conda environment
- Python available inside that same environment
- HuggingFace token if required (edit `batch_transcribe.bat`)

##### **2. Installation**

- Unzip everything into a folder, e.g., `C:\TranscriptionSystem`
- Make sure the structure looks like:

```TranscriptionSystem/
├─ batch_transcribe.bat
├─ convert_json_to_tsv.py
├─ combine_tsvs_with_colors.py
├─ config.json
├─ colors.png
├─ README.txt
└─ whisperx_output/   (empty to start)
```
##### **3. Running It**

- Drag and drop a folder full of .flac files onto batch_transcribe.bat
- Wait for it to finish.
- Find results inside /whisperx_output/

---

#### **Customization**

---

##### **Add or Update Campaigns / Players**

Open `config.json` and edit:

```
{

  "Waterdeep": {

    "benasmaelwys": "Jake",

    "brynmorstonefist": "Saman",

    "cyrnakdatsarb": "Pip",

    "anotheregostar": "Cote",

    "dbuke": "Tinkler"

  },

  "Candlekeep": {

    "benasmaelwys": "Jake",

    "brynmorstonefist": "Old Tsu",

    "cyrnakdatsarb": "Carric",

    "anotheregostar": "Traveller",

    "dbuke": "Lumpy"

  }

}
```

##### **Add new campaigns**:  
Just add a new top-level section, e.g.:

```
"Icewind Dale": {

  "newhandle": "New Character"

}
```


##### **Add new players**:  
Inside an existing campaign, just add another "handle": "Character" line.

##### **Important**:

- Don't leave a trailing comma after the last player.
- Player handle must match the filename (minus the number before the hyphen).

---

#### **Change Output Folder**

By default, outputs go into:

`[Audio Folder]\whisperx_output\`

If you want a different location:
- Open `batch_transcribe.bat`
- Search for `output_root=`
- Change the path logic there.

Example to save always to `C:\Transcripts:`
set `"output_root=C:\Transcripts"`

---

##### **Color Customization**

The Excel (`full_transcript.xlsx`) uses a rotating color palette to separate speakers visually.

**To modify colors**:

- Open `combine_tsvs_with_colors.py`
- Find the `colors = [...]` list
- Add, remove, or reorder colors.

---

##### **Troubleshooting**

| **Problem**        | **Solution**                                                  |
| ------------------ | ------------------------------------------------------------- |
| WhisperX fails     | Check HuggingFace Token, Conda environment                    |
| Output missing     | Ensure filenames match patterns (e.g., numbers-handle_0.flac) |
| Transcript jumbled | Fix missing speaker mapping in `config.json`                  |
| Permission error   | Don't open files in Excel/Notepad while processing            |
| Slips/missing text | Upgrade WhisperX if needed                                    |

---

##### **Cleaner Transcriptions**

This system groups words together based on **pauses** (default = 1 second).

If you want **longer** or **shorter** sentence groupings:

- Open `convert_json_to_tsv.py`
- Find `MAX_PAUSE_SECONDS`
- Adjust value (e.g., `0.8` for tighter, `2.0` for longer).
