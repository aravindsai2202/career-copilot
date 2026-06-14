import json
import streamlit as st
from datetime import datetime

from services.gemini_service import (
    generate_response,
    analyze_resume,
    generate_roadmap,
    match_job_description,
    generate_interview_questions,
    analyze_skill_gap,
)

from utils.memory import add_message
from utils.resume_parser import extract_text_from_pdf


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Career Copilot",
    page_icon="🚀",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

.stApp {
    background: #050B18;
    font-family: 'Space Grotesk', sans-serif;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(circle at 20% 30%, rgba(0, 212, 255, 0.06) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(124, 58, 237, 0.08) 0%, transparent 50%),
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 48px 48px, 48px 48px;
    pointer-events: none;
    z-index: 0;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    position: relative;
    z-index: 1;
}

.hud-eyebrow {
    text-align: center;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: #00D4FF;
    margin-bottom: 12px;
    opacity: 0.8;
}

.hud-title-wrap { text-align: center; margin-bottom: 6px; }

.hud-title {
    font-family: 'Syne', sans-serif;
    font-size: 108px;
    font-weight: 800;
    line-height: 0.95;
    letter-spacing: -4px;
    background: linear-gradient(135deg, #FFFFFF 0%, #A5C8FF 50%, #00D4FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: inline-block;
}

.hud-title-glow {
    display: block;
    width: 220px;
    height: 2px;
    margin: 10px auto 0;
    background: linear-gradient(90deg, transparent, #00D4FF, transparent);
    border-radius: 2px;
    box-shadow: 0 0 16px #00D4FF, 0 0 40px rgba(0,212,255,0.4);
}

.hud-subtitle {
    text-align: center;
    font-size: 18px;
    font-weight: 300;
    color: rgba(200, 220, 255, 0.55);
    letter-spacing: 1px;
    margin-top: 18px;
    margin-bottom: 32px;
}

section[data-testid="stSidebar"] {
    display: none !important;
}

[data-testid="collapsedControl"] {
    display: none !important;
}

.section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #00D4FF;
    margin-bottom: 14px;
    opacity: 0.9;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,212,255,0.04) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0,212,255,0.12) !important;
    gap: 4px !important;
    padding: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(160,200,255,0.6) !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(0,212,255,0.15) !important;
    color: #00D4FF !important;
}

.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* File uploader */
[data-testid="stFileUploader"] { max-width: 460px; }

[data-testid="stFileUploaderDropzone"] {
    background: rgba(0, 212, 255, 0.03) !important;
    border: 1.5px dashed rgba(0, 212, 255, 0.35) !important;
    border-radius: 12px !important;
    padding: 1.2rem 1.6rem !important;
    min-height: 70px !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    background: rgba(0, 212, 255, 0.07) !important;
    border-color: rgba(0, 212, 255, 0.65) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    font-size: 12px !important;
    color: rgba(160, 200, 255, 0.6) !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: rgba(0,212,255,0.1) !important;
    border: 1px solid rgba(0,212,255,0.4) !important;
    color: #00D4FF !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(124,58,237,0.15)) !important;
    border: 1px solid rgba(0,212,255,0.4) !important;
    color: #00D4FF !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, rgba(0,212,255,0.28), rgba(124,58,237,0.28)) !important;
    border-color: #00D4FF !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.25) !important;
}

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background: rgba(8,15,30,0.9) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 10px !important;
    color: #E0EEFF !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(0,212,255,0.5) !important;
    box-shadow: 0 0 12px rgba(0,212,255,0.1) !important;
}

/* Result card */
.result-card {
    background: rgba(8, 15, 30, 0.9);
    padding: 28px 32px;
    border-radius: 16px;
    border: 1px solid rgba(0,212,255,0.15);
    box-shadow: 0 0 40px rgba(0,212,255,0.05);
    color: #C8D8F0;
    font-size: 15px;
    line-height: 1.75;
    margin-top: 16px;
}

/* Chat history card in sidebar */
.history-card {
    background: rgba(0,212,255,0.05);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 8px;
    cursor: pointer;
    font-size: 12px;
    color: rgba(180,210,255,0.8);
}

.stAlert {
    background: rgba(0,212,255,0.07) !important;
    border: 1px solid rgba(0,212,255,0.25) !important;
    border-radius: 10px !important;
    color: #A5D8FF !important;
}

hr {
    border: none !important;
    border-top: 1px solid rgba(0,212,255,0.1) !important;
    margin: 1.2rem 0 !important;
}

[data-testid="stChatMessage"] {
    background: rgba(8,15,30,0.7) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea {
    background: rgba(8,15,30,0.9) !important;
    border: 1px solid rgba(0,212,255,0.25) !important;
    border-radius: 14px !important;
    color: #E0EEFF !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(160,200,255,0.35) !important;
}

.stSpinner > div { border-top-color: #00D4FF !important; }

</style>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================
defaults = {
    "history": [],
    "resume_result": None,
    "resume_text": None,
    "roadmap_result": None,
    "jd_match_result": None,
    "interview_result": None,
    "skill_gap_result": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val








# ==================================================
# HERO
# ==================================================
st.markdown('<div class="hud-eyebrow">AI · Career Intelligence · v3.0</div>', unsafe_allow_html=True)
st.markdown("""
<div class="hud-title-wrap">
    <span class="hud-title">Career Copilot</span>
    <span class="hud-title-glow"></span>
</div>
""", unsafe_allow_html=True)
st.markdown('<p class="hud-subtitle">Navigate your future with precision</p>', unsafe_allow_html=True)


# ==================================================
# TABS
# ==================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 Chat",
    "📄 Resume",
    "🎯 Skill Gap",
    "🎤 Interview",
    "🗺️ Roadmap",
    "🔍 JD Match"
])


# ── TAB 1: CHAT ──────────────────────────────────
with tab1:

    st.markdown('<div class="section-label">AI Career Chat</div>', unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown(
            f"<div style='font-size:11px;color:rgba(0,212,255,0.5);margin-bottom:12px;'>{len(st.session_state.history)} messages in current session</div>",
            unsafe_allow_html=True
        )

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask about careers, roles, interviews, skill gaps...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        add_message(st.session_state.history, "user", user_input)

        with st.spinner("Thinking..."):
            try:
                response = generate_response(user_input, st.session_state.history)
            except Exception as e:
                response = f"Error: {e}"

        with st.chat_message("assistant"):
            st.markdown(response)
        add_message(st.session_state.history, "assistant", response)


# ── TAB 2: RESUME ────────────────────────────────
with tab2:

    st.markdown('<div class="section-label">Resume Analysis</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

    if uploaded_file:
        st.success("Resume uploaded — ready to analyze.")
        try:
            st.session_state.resume_text = extract_text_from_pdf(uploaded_file)

            if st.button("📊 Analyze Resume"):
                with st.spinner("Analyzing your resume..."):
                    st.session_state.resume_result = analyze_resume(st.session_state.resume_text)

            if st.session_state.resume_result:
                st.markdown('<div class="section-label" style="margin-top:20px;">Analysis Report</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-card">{st.session_state.resume_result}</div>', unsafe_allow_html=True)
                st.download_button(
                    label="⬇️ Download Analysis",
                    data=st.session_state.resume_result,
                    file_name="resume_analysis.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error: {e}")


# ── TAB 3: SKILL GAP ─────────────────────────────
with tab3:

    st.markdown('<div class="section-label">Skill Gap Analysis</div>', unsafe_allow_html=True)

    current_skills = st.text_area(
        "Your Current Skills",
        placeholder="e.g. Python, SQL, Excel, Data Analysis, Machine Learning basics...",
        height=100
    )
    col1, col2 = st.columns(2)
    with col1:
        target_role_sg = st.text_input("Target Role", placeholder="e.g. Data Scientist")
    with col2:
        exp_level_sg = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level"])

    if st.button("🔍 Analyze Skill Gap"):
        if current_skills and target_role_sg:
            with st.spinner("Analyzing skill gap..."):
                st.session_state.skill_gap_result = analyze_skill_gap(current_skills, target_role_sg, exp_level_sg)
        else:
            st.warning("Please fill in your skills and target role.")

    if st.session_state.skill_gap_result:
        st.markdown(f'<div class="result-card">{st.session_state.skill_gap_result}</div>', unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Skill Gap Report",
            data=st.session_state.skill_gap_result,
            file_name="skill_gap_analysis.txt",
            mime="text/plain"
        )


# ── TAB 4: INTERVIEW ─────────────────────────────
with tab4:

    st.markdown('<div class="section-label">Interview Preparation</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        interview_role = st.text_input("Role", placeholder="e.g. Software Engineer")
    with col2:
        interview_exp = st.selectbox("Level", ["Fresher", "Mid Level", "Senior", "Lead/Manager"])
    with col3:
        interview_type = st.selectbox("Interview Type", [
            "Technical", "Behavioral", "HR/Cultural Fit",
            "System Design", "Case Study", "Mixed"
        ])

    if st.button("🎤 Generate Interview Questions"):
        if interview_role:
            with st.spinner("Preparing your interview questions..."):
                st.session_state.interview_result = generate_interview_questions(
                    interview_role, interview_exp, interview_type
                )
        else:
            st.warning("Please enter the role.")

    if st.session_state.interview_result:
        st.markdown(f'<div class="result-card">{st.session_state.interview_result}</div>', unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Interview Questions",
            data=st.session_state.interview_result,
            file_name="interview_prep.txt",
            mime="text/plain"
        )


# ── TAB 5: ROADMAP ───────────────────────────────
with tab5:

    st.markdown('<div class="section-label">Career Roadmap</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        current_role = st.text_input("Current Role", placeholder="e.g. Junior Developer")
    with col2:
        target_role = st.text_input("Target Role", placeholder="e.g. ML Engineer")
    with col3:
        experience = st.selectbox("Experience", ["0–1 years", "1–3 years", "3–5 years", "5+ years"])

    if st.button("🗺️ Generate Roadmap"):
        if current_role and target_role:
            with st.spinner("Building your career roadmap..."):
                st.session_state.roadmap_result = generate_roadmap(current_role, target_role, experience)
        else:
            st.warning("Please fill in both current and target roles.")

    if st.session_state.roadmap_result:
        st.markdown(f'<div class="result-card">{st.session_state.roadmap_result}</div>', unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Roadmap",
            data=st.session_state.roadmap_result,
            file_name="career_roadmap.txt",
            mime="text/plain"
        )


# ── TAB 6: JD MATCH ──────────────────────────────
with tab6:

    st.markdown('<div class="section-label">Job Description Matcher</div>', unsafe_allow_html=True)

    if st.session_state.resume_text:
        st.success("✅ Resume loaded from Resume tab.")
        resume_for_jd = st.session_state.resume_text
    else:
        st.info("Upload your resume in the Resume tab first, or paste it below.")
        resume_for_jd = st.text_area("Paste Resume Text", placeholder="Paste your resume content here...", height=150)

    job_description = st.text_area("Paste Job Description", placeholder="Paste the full job description here...", height=200)

    if st.button("🔍 Match Resume to JD"):
        if resume_for_jd and job_description:
            with st.spinner("Analyzing match..."):
                st.session_state.jd_match_result = match_job_description(resume_for_jd, job_description)
        else:
            st.warning("Please provide both resume and job description.")

    if st.session_state.jd_match_result:
        st.markdown(f'<div class="result-card">{st.session_state.jd_match_result}</div>', unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Match Report",
            data=st.session_state.jd_match_result,
            file_name="jd_match_report.txt",
            mime="text/plain"
        )