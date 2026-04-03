from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import email
from bs4 import BeautifulSoup
import requests
import json

app = FastAPI()

OLLAMA_URL = "http://localhost:11434"
MODEL = "gpt-oss:20b"


# =========================
# HTML TEMPLATE
# =========================

def render_page(content=""):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Phishing Analyzer</title>
    <style>
        body {{ font-family: Arial; padding: 40px; background: #f5f5f5; }}
        .box {{ background: white; padding: 20px; border-radius: 10px; }}
        .result {{
            margin-top: 20px;
            padding: 20px;
            background: #111;
            color: #0f0;
            border-radius: 10px;
            white-space: pre-wrap;
        }}
        button {{
            margin-top: 10px;
            padding: 10px 15px;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="box">
        <h2>Upload .eml file</h2>
        <form action="/analyze" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <br>
            <button type="submit">Analyze</button>
        </form>
        {content}
    </div>
</body>
</html>
"""

# =========================
# ROUTES
# =========================

@app.get("/", response_class=HTMLResponse)
def home():
    return render_page()

@app.get("/analyze", response_class=HTMLResponse)
def analyze_get():
    return render_page("<div class='result'>⚠️ Please upload a file using the form.</div>")

# =========================
# EMAIL PARSER
# =========================

def extract_email_content(raw_bytes):
    msg = email.message_from_bytes(raw_bytes)
    text = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                text += part.get_payload(decode=True).decode(errors="ignore")
            elif content_type == "text/html":
                html = part.get_payload(decode=True).decode(errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                text += soup.get_text()
    else:
        text = msg.get_payload(decode=True).decode(errors="ignore")

    return text.strip()

# =========================
# OLLAMA CALL 
# =========================

def analyze_with_llm(content):
    # Truncate to avoid overwhelming the model
    content = content[:6000]

    prompt = f"""
You are a cybersecurity analyst.

Analyze the email below and return STRICT JSON only — no markdown, no explanation.

Expected format:
{{
  "sender_intent": "",
  "is_phishing": true,
  "urgency": true,
  "summary": "",
  "suspicious_elements": []
}}

Email:
{content}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()

        data = response.json()
        llm_text = data.get("response", "").strip()

        # Strip markdown code fences if present
        if llm_text.startswith("```"):
            llm_text = llm_text.split("```")[1]
            if llm_text.startswith("json"):
                llm_text = llm_text[4:]
            llm_text = llm_text.strip()

        try:
            return json.loads(llm_text)
        except json.JSONDecodeError:
            return {
                "sender_intent": "unknown",
                "is_phishing": False,
                "urgency": False,
                "summary": llm_text or "Could not parse LLM response.",
                "suspicious_elements": []
            }

    except Exception as e:
        return {"error": str(e)}

# =========================
# FORMAT OUTPUT
# =========================

def format_output(result):
    if "error" in result:
        return f"<div class='result'>❌ ERROR:<br>{result['error']}</div>"

    formatted = f"""
🔍 PHISHING ANALYSIS

🧠 Intent: {result.get('sender_intent')}
⚠️ Phishing: {result.get('is_phishing')}
🔥 Urgency: {result.get('urgency')}

📝 Summary:
{result.get('summary')}

🚨 Suspicious Elements:
- """ + "<br>- ".join(result.get("suspicious_elements", []))

    return f"<div class='result'>{formatted}</div>"

# =========================
# ANALYZE ENDPOINT
# =========================

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(file: UploadFile = File(...)):
    raw = await file.read()

    # basic protection
    if len(raw) > 2_000_000:
        return render_page("<div class='result'>❌ File too large</div>")

    content = extract_email_content(raw)

    if not content:
        return render_page("<div class='result'>❌ Could not extract email content</div>")

    result = analyze_with_llm(content)
    formatted = format_output(result)

    return render_page(formatted)

# =========================
# RUN
# =========================
# uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
