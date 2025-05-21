# 🎙️ Using Craig Bot to Record Discord Audio (.flac)

This guide walks you through how to use the [Craig Discord bot](https://craig.chat/) to record your voice channels and export individual `.flac` files for use with the WhisperX transcription pipeline.

---

## 🛠️ Setup

### Step 1: Invite Craig to Your Server

1. Go to [https://craig.chat/home/](https://craig.chat/home/)
2. Click “Invite Craig to your Discord server”
3. Authorize Craig with appropriate permissions

### Step 2: Basic Recording Command

To start a recording, enter this in any text channel:

```
:craig:, join
```

Craig will join the **voice channel you're in** and begin recording.

---

## ⏹️ Stop Recording

To stop the recording and have Craig leave:

```
:craig:, leave
```

Craig will DM you (or the server owner) a link to download the recordings.

---

## 🎧 Downloading .flac Files

After stopping the recording:

1. Open the DM from Craig
2. Click the link to access the session page
3. Choose the **"Separate Tracks (FLAC)"** download option

This will give you a `.zip` file containing one `.flac` file per speaker.

---

## 📁 Preparing Files for Transcription

1. Unzip the Craig `.zip` into a folder (e.g., `Session_2025-05-21`)
2. Rename each file to follow this format:
   ```
   001-handle_0.flac
   002-handle_0.flac
   ...
   ```
   - Replace `handle` with the Discord username (or the config mapping key)
   - Keep numbers sequential

> 💡 Optional: Use the included `rename_files.py` to auto-rename if mapped in `config.json`.

---

## 🔁 Then What?

Drag your folder of `.flac` files onto `1 - Create Transcripts.bat` to start the full WhisperX transcription pipeline.

---

## 🧾 Notes

- Craig records separate audio per speaker (perfect for this system)
- Craig only records **while users are in the voice channel**
- Recordings expire after ~7 days unless downloaded

---

## 📎 Useful Links

- [Craig Bot Home](https://craig.chat/home/)
- [Craig Help Commands](https://craig.chat/home/help/)
- [WhisperX Transcription README](./README_TranscriptionSystem.md)

---
