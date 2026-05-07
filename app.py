import streamlit as st
import pdfplumber
import requests
import json
import google.generativeai as genai
import re

# ─────────────────────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Document Orchestrator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
#  CSS — Dark Cyber-Minimal Theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Outfit:wght@300;400;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

.stApp {
    background: #080c14;
    color: #e2e8f0;
    min-height: 100vh;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1300px; }

/* ── Hero Header ── */
.hero {
    position: relative;
    text-align: center;
    padding: 3rem 0 2.5rem;
    margin-bottom: 1rem;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%; transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse, rgba(0,245,160,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00f5a0;
    border: 1px solid rgba(0,245,160,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 3.2rem;
    line-height: 1.1;
    margin: 0 0 0.75rem 0;
    background: linear-gradient(135deg, #ffffff 0%, #00f5a0 50%, #00d9f5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: #64748b;
    font-size: 1rem;
    font-family: 'JetBrains Mono', monospace;
    margin: 0;
}

/* ── Stage Header ── */
.stage-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.2rem;
    margin-top: 0.5rem;
}
.stage-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 2px;
    color: #080c14;
    background: linear-gradient(90deg, #00f5a0, #00d9f5);
    border-radius: 4px;
    padding: 3px 8px;
}
.stage-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
}
.stage-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(0,245,160,0.3), transparent);
}

/* ── Upload Card ── */
.upload-zone {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.8rem;
}

/* ── File uploader override ── */
[data-testid="stFileUploader"] {
    background: rgba(0,245,160,0.03) !important;
    border: 1.5px dashed rgba(0,245,160,0.25) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] label { color: #94a3b8 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(90deg, #00f5a0, #00d9f5) !important;
    color: #080c14 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    box-shadow: 0 0 20px rgba(0,245,160,0.15) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 0 30px rgba(0,245,160,0.3) !important;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
    margin: 2.5rem 0;
}

/* ── Table override ── */
[data-testid="stTable"] table {
    background: transparent !important;
    border: none !important;
}
[data-testid="stTable"] th {
    background: rgba(0,245,160,0.08) !important;
    color: #00f5a0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border: none !important;
    padding: 10px 16px !important;
}
[data-testid="stTable"] td {
    color: #e2e8f0 !important;
    border: none !important;
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    padding: 10px 16px !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stTable"] tr:hover td { background: rgba(255,255,255,0.02) !important; }

/* ── Output Cards ── */
.out-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    height: 100%;
}
.out-card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #00d9f5;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.out-card-label span {
    display: inline-block;
    width: 18px; height: 18px;
    background: rgba(0,217,245,0.15);
    border-radius: 50%;
    text-align: center;
    line-height: 18px;
    font-size: 0.6rem;
    color: #00d9f5;
}
.out-card-body {
    font-family: 'Outfit', sans-serif;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.7;
    white-space: pre-wrap;
}

/* ── Risk badges ── */
.risk-high {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    color: #fca5a5;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 1rem;
}
.risk-medium {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(251,191,36,0.1);
    border: 1px solid rgba(251,191,36,0.35);
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    color: #fde68a;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 1rem;
}
.risk-low {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(0,245,160,0.08);
    border: 1px solid rgba(0,245,160,0.25);
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    color: #6ee7b7;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

/* ── Status blocks ── */
.status-sent {
    background: rgba(0,245,160,0.08);
    border: 1px solid rgba(0,245,160,0.4);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: #00f5a0;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 1rem;
    text-align: center;
    letter-spacing: 1px;
}
.status-not-sent {
    background: rgba(251,191,36,0.08);
    border: 1px solid rgba(251,191,36,0.3);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: #fbbf24;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.9rem;
    text-align: center;
}

/* ── Text inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(0,245,160,0.4) !important;
    box-shadow: 0 0 0 2px rgba(0,245,160,0.1) !important;
}

/* ── Info box ── */
[data-testid="stAlert"] {
    background: rgba(0,217,245,0.06) !important;
    border: 1px solid rgba(0,217,245,0.2) !important;
    border-radius: 10px !important;
    color: #93c5fd !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #1e293b;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    padding: 2rem 0 1rem;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  Hero
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">⚡ AI-Powered · Business Process Automation</div>
    <h1>Document Orchestrator</h1>
    <p>upload → extract → analyze → automate</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  Secrets
# ─────────────────────────────────────────────────────────────
try:
    GEMINI_API_KEY  = st.secrets["GEMINI_API_KEY"]
    N8N_WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.error("⚠️ Add GEMINI_API_KEY and N8N_WEBHOOK_URL to .streamlit/secrets.toml")
    st.stop()

# ─────────────────────────────────────────────────────────────
#  Session State
# ─────────────────────────────────────────────────────────────
for k in ["doc_text", "extracted_json", "n8n_result", "user_question"]:
    if k not in st.session_state:
        st.session_state[k] = None

# ─────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────
def call_gemini(prompt, max_tokens=500):
    """Direct call to Google Gemini via google-generativeai SDK."""
    model = genai.GenerativeModel(
        model_name="gemini-flash-latest",
        generation_config=genai.GenerationConfig(max_output_tokens=max_tokens)
    )
    response = model.generate_content(prompt)
    return response.text.strip()
# import time

# def call_gemini(prompt, max_tokens=800):
#     model = genai.GenerativeModel(
#         model_name="gemini-1.5-flash-8b",
#         generation_config=genai.GenerationConfig(max_output_tokens=max_tokens)
#     )
#     for attempt in range(3):  # retry 3 times
#         try:
#             response = model.generate_content(prompt)
#             return response.text.strip()
#         except Exception as e:
#             if "429" in str(e) or "quota" in str(e).lower():
#                 wait = (attempt + 1) * 15  # wait 15s, 30s, 45s
#                 st.warning(f"⏳ Quota limit hit. Retrying in {wait}s...")
#                 time.sleep(wait)
#             else:
#                 raise e
#     raise Exception("Gemini quota exhausted. Please wait a minute and try again.")

def extract_text(file):
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    return file.read().decode("utf-8", errors="ignore")

# def extract_with_ai(doc_text, question):
#     prompt = (
#         "You are an expert document analyst.\n\n"
#         f"DOCUMENT:\n\"\"\"{doc_text[:3000]}\"\"\"\n\n"
#         f"USER QUESTION: {question}\n\n"
#         "TASK:\n"
#         "1. Extract 5-8 most relevant key-value pairs that directly answer the question.\n"
#         "2. Add risk_level: High if overdue/penalty/breach/lawsuit/termination/legal/default/unpaid, "
#         "Medium if delayed/dispute/warning/partial payment, Low otherwise.\n"
#         "3. Return ONLY valid JSON. No markdown, no explanation, no code fences.\n\n"
#         'Example: {"invoice_no": "INV-001", "amount_due": "50000", "risk_level": "High"}'
#     )
#     raw = call_gemini(prompt, max_tokens=500)
#     if raw.startswith("```"):
#         raw = raw.split("```")[1]
#         if raw.startswith("json"):
#             raw = raw[4:]
#     return json.loads(raw.strip())
def extract_with_ai(doc_text, question):
    prompt = (
        "You are an expert document analyst.\n\n"
        f"DOCUMENT:\n\"\"\"{doc_text[:3000]}\"\"\"\n\n"
        f"USER QUESTION: {question}\n\n"
        "TASK:\n"
        "1. Extract 5-8 most relevant key-value pairs that directly answer the question.\n"
        "2. Add risk_level: High if overdue/penalty/breach/lawsuit/termination/legal/default/unpaid, "
        "Medium if delayed/dispute/warning/partial payment, Low otherwise.\n"
        "3. Return ONLY a raw JSON object. No markdown, no code fences, no explanation, no extra text.\n\n"
        'Example output: {"invoice_no": "INV-001", "amount_due": "50000", "risk_level": "High"}'
    )
    raw = call_gemini(prompt, max_tokens=800)  # increased tokens to avoid truncation

    # Strip markdown code fences if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()

    # Extract JSON object using regex if extra text surrounds it
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        raw = match.group(0)

    return json.loads(raw)
def generate_final_answer(doc_text, extracted_data, question):
    prompt = (
        "You are a professional document analyst.\n\n"
        f"Document:\n{doc_text[:2000]}\n\n"
        f"Question: {question}\n"
        f"Extracted Data: {json.dumps(extracted_data)}\n\n"
        "Provide a clear, professional analytical answer referencing specific values."
    )
    return call_gemini(prompt, max_tokens=400)

def generate_email_body(extracted_data, question, final_answer):
    prompt = (
        "Write a formal HIGH RISK ALERT email body.\n\n"
        f"Risk Data: {json.dumps(extracted_data)}\n"
        f"Question: {question}\n\n"
        "Requirements: Start with Dear Sir/Madam, state HIGH RISK alert, "
        "list risk findings with values, recommend action, "
        "end with Regards, AI Document Orchestrator System. No Subject line. No markdown."
    )
    return call_gemini(prompt, max_tokens=400)

def trigger_n8n_email(doc_text, extracted_data, question, recipient_email):
    payload = {
        "document_text":  doc_text[:3000],
        "user_question":  question,
        "extracted_data": extracted_data,
        "recipient_email": recipient_email
    }
    try:
        resp = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=60)
        return resp.status_code == 200
    except Exception:
        return False
# def trigger_n8n_email(doc_text, extracted_data, question, recipient_email):
#     payload = {
#         "document_text":  doc_text[:3000],
#         "user_question":  question,
#         "extracted_data": extracted_data,
#         "recipient_email": recipient_email
#     }
#     try:
#         resp = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=60)
#         st.write("🔗 Webhook URL:", N8N_WEBHOOK_URL)
#         st.write("📬 Status code:", resp.status_code)
#         st.write("📬 Response:", resp.text)
#         return resp.status_code == 200
#     except Exception as e:
#         st.write("❌ Exception:", str(e))
#         return False


# ═══════════════════════════════════════════════════════════════
#  STAGE 1 — Document Upload & Query
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="stage-wrap">
    <div class="stage-num">STAGE 01</div>
    <div class="stage-title">Document Upload &amp; Query</div>
    <div class="stage-line"></div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")
with col1:
    uploaded_file = st.file_uploader(
        "Upload your document",
        type=["pdf", "txt"],
        help="Supported formats: PDF, TXT"
    )
with col2:
    question_input = st.text_area(
        "Your analytical question",
        placeholder="e.g. What are the overdue payment risks and legal consequences?",
        height=130
    )

st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([2, 1.5, 2])
with btn_col:
    extract_btn = st.button("⚡ Extract & Analyse", use_container_width=True)

if extract_btn:
    if not uploaded_file:
        st.warning("Please upload a PDF or TXT file.")
    elif not question_input.strip():
        st.warning("Please enter an analytical question.")
    else:
        with st.spinner("📖 Reading document..."):
            text = extract_text(uploaded_file)
            st.session_state.doc_text = text
            st.session_state.user_question = question_input.strip()
            st.session_state.n8n_result = None

        with st.spinner("🤖 Extracting structured data with AI..."):
            try:
                result = extract_with_ai(text, question_input.strip())
                st.session_state.extracted_json = result
                st.success("✅ Extraction complete!")
            except json.JSONDecodeError as e:
                st.error(f"AI returned invalid JSON: {e}")
            except Exception as e:
                st.error(f"Extraction error: {e}")


# ═══════════════════════════════════════════════════════════════
#  STAGE 2 — Structured Data Extraction
# ═══════════════════════════════════════════════════════════════
if st.session_state.extracted_json:
    data = st.session_state.extracted_json

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="stage-wrap">
        <div class="stage-num">STAGE 02</div>
        <div class="stage-title">Structured Data Extracted</div>
        <div class="stage-line"></div>
    </div>
    """, unsafe_allow_html=True)

    st.table([{"Field": k, "Value": str(v)} for k, v in data.items()])

    with st.expander("🔍 View raw JSON"):
        st.json(data)


    # ═══════════════════════════════════════════════════════════
    #  STAGE 3 — Email Alert Automation
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="stage-wrap">
        <div class="stage-num">STAGE 03</div>
        <div class="stage-title">Email Alert Automation (n8n)</div>
        <div class="stage-line"></div>
    </div>
    """, unsafe_allow_html=True)

    risk = data.get("risk_level", "N/A")
    if risk == "High":
        st.markdown('<div class="risk-high">🔴 &nbsp; Risk Level: HIGH — Alert email WILL be sent via n8n</div>',
                    unsafe_allow_html=True)
    elif risk == "Medium":
        st.markdown('<div class="risk-medium">🟡 &nbsp; Risk Level: MEDIUM — Email will NOT be sent (requires High)</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="risk-low">🟢 &nbsp; Risk Level: LOW — Email will NOT be sent (requires High)</div>',
                    unsafe_allow_html=True)

    col_email, col_btn = st.columns([2, 1], gap="medium")
    with col_email:
        recipient_email = st.text_input(
            "Recipient Email ID",
            placeholder="recipient@example.com",
            label_visibility="collapsed"
        )
    with col_btn:
        send_btn = st.button("📨 Send Alert Mail", use_container_width=True)

    if send_btn:
        if not recipient_email.strip():
            st.warning("Please enter a recipient email address.")
        else:
            final_answer = ""
            email_body   = ""
            status       = ""

            with st.spinner("🧠 Generating analytical answer..."):
                try:
                    final_answer = generate_final_answer(
                        st.session_state.doc_text,
                        st.session_state.extracted_json,
                        st.session_state.user_question
                    )
                except Exception as e:
                    final_answer = f"Could not generate answer: {e}"

            if risk == "High":
                with st.spinner("✍️ Drafting alert email..."):
                    try:
                        email_body = generate_email_body(
                            st.session_state.extracted_json,
                            st.session_state.user_question,
                            final_answer
                        )
                    except Exception as e:
                        email_body = f"Could not generate email: {e}"

                with st.spinner("📨 Sending email via n8n..."):
                    sent   = trigger_n8n_email(
                        st.session_state.doc_text,
                        st.session_state.extracted_json,
                        st.session_state.user_question,
                        recipient_email.strip()
                    )
                    status = "SENT" if sent else "EMAIL SEND FAILED — check n8n activation"
            else:
                email_body = "Risk level is not High. No alert email was sent by n8n."
                status     = "Condition Not Met"

            st.session_state.n8n_result = {
                "final_answer": final_answer,
                "email_body":   email_body,
                "status":       status
            }
            st.success("✅ Workflow complete!")


# ═══════════════════════════════════════════════════════════════
#  STAGE 4 — Four Required Outputs
# ═══════════════════════════════════════════════════════════════
if st.session_state.n8n_result:
    result = st.session_state.n8n_result

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="stage-wrap">
        <div class="stage-num">STAGE 04</div>
        <div class="stage-title">Final Outputs</div>
        <div class="stage-line"></div>
    </div>
    """, unsafe_allow_html=True)

    top_l, top_r = st.columns(2, gap="large")

    # ① Structured Data
    with top_l:
        st.markdown("""
        <div class="out-card-label">
            <span>①</span> Structured Data Extracted
        </div>
        """, unsafe_allow_html=True)
        st.json(st.session_state.extracted_json)

    # ② Final Analytical Answer
    with top_r:
        st.markdown("""
        <div class="out-card-label">
            <span>②</span> Final Analytical Answer
        </div>
        """, unsafe_allow_html=True)
        answer = result.get("final_answer", "No answer returned.")
        st.markdown(f'<div class="out-card"><div class="out-card-body">{answer}</div></div>',
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    bot_l, bot_r = st.columns(2, gap="large")

    # ③ Generated Email Body
    with bot_l:
        st.markdown("""
        <div class="out-card-label">
            <span>③</span> Generated Email Body
        </div>
        """, unsafe_allow_html=True)
        email_body = result.get("email_body", "No email body returned.")
        st.markdown(f'<div class="out-card"><div class="out-card-body">{email_body}</div></div>',
                    unsafe_allow_html=True)

    # ④ Email Automation Status
    with bot_r:
        st.markdown("""
        <div class="out-card-label">
            <span>④</span> Email Automation Status
        </div>
        """, unsafe_allow_html=True)
        status = result.get("status", "UNKNOWN")
        if "SENT" in status.upper():
            st.markdown(
                '<div class="status-sent">✅&nbsp;&nbsp;Alert Email Status: SENT</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="status-not-sent">⚠️&nbsp;&nbsp;Status: {status}</div>',
                unsafe_allow_html=True
            )

# ─────────────────────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">AI-POWERED DOCUMENT ORCHESTRATOR &nbsp;·&nbsp; '
    'STREAMLIT + GOOGLE GEMINI + N8N</div>',
    unsafe_allow_html=True
)