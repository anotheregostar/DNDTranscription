# 🧰 Python Environment Setup Guide

This guide outlines the required Python libraries and dependencies for running the full transcription automation project, including WhisperX and all enhancement scripts.

---

## ✅ Requirements

- Python 3.8–3.10
- Conda (Miniconda or Anaconda)
- Git

---

## 🛠️ 1. Create and Activate Conda Environment

```bash
conda create -n whisperx python=3.9 -y
conda activate whisperx
```

---

## 📦 2. Install Core Dependencies

### WhisperX (with all required packages)

```bash
pip install git+https://github.com/m-bain/whisperx.git
```

WhisperX will install:
- `torch`, `torchaudio`, `transformers`, `faster-whisper`, `whisperx`, etc.

> 🔍 If using a CUDA GPU, install the compatible PyTorch build (adjust `cu118` based on your version):

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

> 💻 For CPU-only systems:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

---

## 🧰 3. Install Additional Project Libraries

These are needed for glossary processing, Excel output, and anomaly detection:

```bash
pip install pandas openpyxl python-Levenshtein pyspellchecker jellyfish
```

If you want colored console output or rich logs:

```bash
pip install rich
```

---

## 🔄 4. Optional: Install FFmpeg (for audio conversion)

WhisperX depends on `ffmpeg` being available in your system path.

- [Download FFmpeg for Windows](https://www.gyan.dev/ffmpeg/builds/)
- Extract and add the `/bin` folder to your `PATH` environment variable

Check it works:

```bash
ffmpeg -version
```

---

## ✅ 5. Verify Everything Works

Test imports:

```python
import whisperx
import pandas as pd
import openpyxl
import Levenshtein
import jellyfish
from spellchecker import SpellChecker
```

If no errors are raised — you're good to go!

---

## 🔗 Related Docs

- [WhisperX Setup Guide](./WhisperX_Setup_Guide.md)
- [Main Transcription README](./README_TranscriptionSystem.md)

---
