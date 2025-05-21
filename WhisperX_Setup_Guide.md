# 🧠 WhisperX Installation & Setup Guide

This guide walks you through installing WhisperX in a Conda environment and preparing your system to run the transcription automation suite.

---

## ✅ System Requirements

- Windows (recommended)
- An NVIDIA GPU (for faster transcription using CUDA)
- Python 3.8+
- Miniconda or Anaconda installed

---

## 🛠 Step-by-Step Setup

### 1. Install Conda (if not already installed)

- [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/)

### 2. Create and Activate a Conda Environment

```bash
conda create -n whisperx python=3.9 -y
conda activate whisperx
```

### 3. Install WhisperX and Dependencies

```bash
pip install git+https://github.com/m-bain/whisperx.git
```

> ℹ️ WhisperX will install PyTorch, torchaudio, transformers, and other dependencies.

If you have a CUDA-compatible GPU, install the proper PyTorch version:

```bash
# Check your CUDA version, then run something like:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

To use CPU only:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 4. (Optional) HuggingFace Token

If you're using speaker diarization or models from HuggingFace:

1. Create a HuggingFace account: https://huggingface.co
2. Generate an access token
3. Paste the token into `batch_transcribe.bat` like:

```bat
set HF_TOKEN=your_token_here
```

---

## 🔁 Test Your Setup

Run the following Python snippet to confirm WhisperX is installed correctly:

```python
import whisperx
print("✅ WhisperX is ready!")
```

---

## 📦 Next Step

Once WhisperX is working:

- Place your `.flac` files in a folder
- Drag that folder onto `1 - Create Transcripts.bat`
- Let the automation do the rest!

---

## 🔗 Related Links

- [WhisperX GitHub](https://github.com/m-bain/whisperx)
- [PyTorch Installation Help](https://pytorch.org/get-started/locally/)

---
