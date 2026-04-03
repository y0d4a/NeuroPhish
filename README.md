# 🛡️ PhishEye

Simple web app for analyzing `.eml` emails using a local LLM (Ollama).

---

## 🚀 Quick Start

### 1. Clone repo

```bash
git clone https://github.com/yourusername/phisheye.git
cd phisheye
```

---

### 2. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull gpt-oss:20b
```

---

### 3. Install uv

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

---

### 4. Install dependencies

```bash
uv init
uv add fastapi uvicorn python-multipart beautifulsoup4 requests
```

---

### 5. Run app

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

### 6. Open in browser

```
http://<server-ip>:8000
```

Upload `.eml` → get phishing analysis.

---

## ⚠️ Notes

* Requires Ollama on `localhost:11434`
* Model: `gpt-oss:20b`
* Demo tool (no auth, no rate limiting)
