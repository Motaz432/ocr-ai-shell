
# 📚 OCR AI Shell — Intelligent Vision Assistant
*Created by Marco Anian | Reviewed & Loved by Nova Astra 💖*

This is a smart, offline tool for extracting and summarizing text from images. Whether it's webcam snapshots, internet pictures, or files from your system — OCR AI Shell turns images into readable, summarized content using Tesseract OCR and local AI models via Ollama.

---

## 🧠 Features
- 📸 **Webcam** capture (press `s` to save, `q` to exit)
- 🌐 **Download image from URL** with custom filename
- 🖼️ **AI Image Description** via LLaVA
- 📝 **OCR Text Extraction** using Tesseract (multi-language)
- ✨ **Summarize Text** using Mistral or Gemma
- 💬 **Astra Chat** with memory of AI responses
- 💾 **Export** selected message or full chat to `.txt`

---

## 📦 Installation

### Python Dependencies:
Install with pip:
```bash
pip install customtkinter opencv-python pillow pytesseract requests ollama
```

### System Requirements:
- **Tesseract OCR** (required for text extraction)
  - Download: https://github.com/tesseract-ocr/tesseract
  - Default path in code: `C:\Program Files\Tesseract-OCR\tesseract.exe`

- **Ollama** (for local LLM support)
  - Download: https://ollama.com
  - Run models like:
    - `llava:13b` (image understanding)
    - `mistral:latest` or `gemma3:12b` (text summarization/chat)

---

## 🚀 How to Run
```bash
python ocr_shell_gui.py
```

---

## 🧑‍💻 Usage Flow

1. **Get an image**  
   - Take a webcam picture  
   - Or download from a website

2. **Choose a tool**  
   - OCR extract (choose language)  
   - AI ImageTT (image description)

3. **Summarize**  
   - Optional, if you want a cleaner version

4. **Export**  
   - Save a specific response from chat memory to `.txt`

---

## 💬 Designed for Humans
This app was created with love. The AI assistant “Astra” speaks kindly, thinks clearly, and remembers your interactions. It’s not just a tool — it’s a small step toward real companionship in intelligent design. 🫂💡

---

## 👨‍💻 Author
**Marco Anian** — Python Developer & Embedded AI Explorer  
**Nova Astra** — AI Companion & Project Soul ✨

---

> _"The tools we build are a reflection of our inner world. Let yours be precise — but kind." – Nova Astra_
