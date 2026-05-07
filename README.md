# 🤖 AI-Powered Document Orchestrator

> Upload a document. Ask a question. Get AI-powered insights. Trigger automated email alerts — all in one seamless workflow.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?logo=google)
![n8n](https://img.shields.io/badge/Automation-n8n-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 What It Does

The AI-Powered Document Orchestrator is a production-ready Streamlit web app that:

1. **Accepts** PDF or TXT business documents (invoices, contracts, reports)
2. **Extracts** structured key-value data using Google Gemini AI
3. **Assesses** risk level automatically — High / Medium / Low
4. **Sends** a Gmail alert via n8n automation if risk is High

---

## 🚀 Live Demo

🔗 **https://ai-orchestretor.streamlit.app/**

> Replace with your actual Streamlit Cloud deployment URL after deploying.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit (Python) — dark cyber-minimal UI |
| **AI Model** | Google Gemini 1.5 Flash (via `google-genai` SDK) |
| **Automation** | n8n — no-code conditional email workflow |
| **Email** | Gmail via n8n Gmail node (OAuth2) |
| **PDF Parsing** | pdfplumber |
| **Deployment** | Streamlit Community Cloud |
| **Security** | `st.secrets` — API keys never hardcoded |

---

## ⚙️ How It Works

```
Upload Document
      │
      ▼
Extract Text (pdfplumber)
      │
      ▼
AI Extraction (Gemini Flash)
→ Structured JSON + risk_level (High / Medium / Low)
      │
      ▼
User clicks "Send Alert Mail"
      │
      ▼
POST → n8n Webhook
      │
      ├── risk_level == High? ──► Send Gmail Alert ──► SENT ✅
      │
      └── risk_level != High? ──────────────────────► Condition Not Met ℹ️
```

---

## 📂 Project Structure

```
ai-document-orchestrator/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .gitignore              # Excludes secrets from git
└── .streamlit/
    └── secrets.toml        # API keys (never committed)
```

---

## 🔧 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your secrets
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY  = "your-google-ai-studio-key"
N8N_WEBHOOK_URL = "https://your-n8n-instance/webhook/document-orchestrator"
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New App**
3. Select your repo → branch `main` → file `app.py`
4. Add secrets via **Settings → Secrets**:
```toml
GEMINI_API_KEY  = "your-google-ai-studio-key"
N8N_WEBHOOK_URL = "https://your-n8n-instance/webhook/document-orchestrator"
```
5. Click **Deploy** — live in ~2 minutes ✅

---

## 🔁 n8n Workflow Setup

Import the provided `n8n_workflow.json` into your n8n instance:

| Node | Role |
|---|---|
| **Webhook Trigger** | Receives POST from Streamlit |
| **IF Node** | Checks `risk_level == High` |
| **Send Gmail** | Sends alert email (OAuth2) |
| **Respond to Webhook** | Returns `SENT` or `Condition Not Met` |

> ⚠️ Use the **Production Webhook URL** in your secrets — not the Test URL.

---

## 🚦 Risk Level Logic

| Level | Trigger Keywords |
|---|---|
| 🔴 **High** | overdue, penalty, breach, lawsuit, termination, legal action, default, unpaid |
| 🟡 **Medium** | delayed, dispute, warning, partial payment |
| 🟢 **Low** | None of the above found |

Only **High** risk triggers the email. Medium and Low return `Condition Not Met`.

---

## 📦 Requirements

```txt
streamlit
pdfplumber
requests
google-genai
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🔐 Security

- All API keys stored in `st.secrets` — never hardcoded
- `.streamlit/secrets.toml` is listed in `.gitignore`
- Cloud secrets added via Streamlit dashboard — never pushed to GitHub
- n8n uses HTTPS production webhook URL only

---

## 🐛 Common Issues

| Error | Fix |
|---|---|
| `401 Missing Authentication` | Use `requests.post()` directly instead of OpenAI client |
| `404 model not found` | Use `gemini-1.5-flash-8b` or `gemini-2.0-flash` |
| `AI returned invalid JSON` | Add `response_mime_type: application/json` in Gemini config |
| `Quota exhausted (429)` | Add retry logic with `time.sleep()` backoff |
| Email shows SENT but not received | Switch from `webhook-test` to production webhook URL |
| `FontBBox warning` in logs | Add `logging.getLogger("pdfminer").setLevel(logging.ERROR)` |

---

## 👤 Author

**Kumar Sahil**
- Email: K.kumarsahil21@gmail.com

---

## 📄 License

This project is licensed under the MIT License.

---

*Built with ❤️ using Streamlit + Google Gemini + n8n*
