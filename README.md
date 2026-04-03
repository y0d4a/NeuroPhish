# 🛡️ NeuroPhish

Simple web app for analyzing `.eml` emails using a local LLM (Ollama).

---

## 🚀 Quick Start

### 1. Clone repo

```bash
git clone https://github.com/y0d4a/phisheye.git
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


<img width="2238" height="753" alt="image" src="https://github.com/user-attachments/assets/ddbfe7a0-43c1-4aba-80dc-d41f5794bcdb" />
<img width="1143" height="603" alt="image" src="https://github.com/user-attachments/assets/09a5b19d-3236-44d0-93ce-d745a6506122" />

