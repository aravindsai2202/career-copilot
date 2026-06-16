# 🚀 Career Copilot

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=20&pause=1000&color=00D4FF&center=true&vCenter=true&width=600&lines=AI+Career+Assistant;Resume+Analysis+%7C+Skill+Gap+%7C+Interview+Prep;Navigate+Your+Future+with+Precision!" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-green"/>
</p>

<p align="center">
  <img src="screenshots/01_home.png" alt="Career Copilot Home" width="100%"/>
</p>

---

## 🤖 What is Career Copilot?

**Career Copilot** is an AI-powered career assistant built with **Streamlit** and **Google Gemini**. It helps you analyze your resume, identify skill gaps, prepare for interviews, plan your career roadmap, and match your profile to job descriptions — all in one sleek dark-themed app.

---

## ✨ Features

| Tab | Feature |
|-----|---------|
| 💬 **Chat** | AI career advisor — ask anything about roles, skills, interviews |
| 📄 **Resume** | Upload PDF → get a detailed AI analysis & download report |
| 🎯 **Skill Gap** | Compare your skills vs your target role |
| 🎤 **Interview** | Generate role-specific interview questions (Technical / HR / System Design) |
| 🗺️ **Roadmap** | Get a step-by-step career roadmap from your current to target role |
| 🔍 **JD Match** | Paste a job description → see how well your resume matches |

---

## 📸 Screenshots

### 💬 AI Career Chat
> Ask anything about careers, roles, interviews, skill gaps

<p align="center">
  <img src="screenshots/02_chat.png" alt="AI Career Chat" width="100%"/>
</p>

---

### 📄 Resume Analysis
> Upload your resume PDF and get a detailed strengths, weaknesses & missing skills report

<p align="center">
  <img src="screenshots/03_resume.png" alt="Resume Analysis" width="100%"/>
</p>

---

### 🎯 Skill Gap Analysis
> Enter your current skills, target role & experience level to see exactly what you're missing

<p align="center">
  <img src="screenshots/04_skill_gap.png" alt="Skill Gap Analysis" width="100%"/>
</p>

---

### 🎤 Interview Preparation
> Generate role-specific questions — Technical, Behavioral, HR, System Design, Case Study & Mixed

<p align="center">
  <img src="screenshots/05_interview.png" alt="Interview Preparation" width="100%"/>
</p>

---

### 🗺️ Career Roadmap
> Get a personalized step-by-step roadmap from your current role to your dream job

<p align="center">
  <img src="screenshots/06_roadmap.png" alt="Career Roadmap" width="100%"/>
</p>

---

### 🔍 JD Match
> Paste a job description and match it against your resume instantly

<p align="center">
  <img src="screenshots/07_jd_match.png" alt="JD Match" width="100%"/>
</p>

---

## 🛠️ Tech Stack

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
</p>

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/aravindsai2202/career-copilot.git
cd career-copilot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.streamlit/secrets.toml` file:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Get your free Gemini API key at 👉 [Google AI Studio](https://aistudio.google.com/app/apikey)

### 4. Run the app
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → **New App**
3. Select this repo and set `app.py` as the entry point
4. Add your secret in **App Settings → Secrets**:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```
5. Click **Deploy** 🎉

---

## 📁 Project Structure

```
career-copilot/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── config/                 # App configuration
├── prompts/                # AI prompt templates
├── screenshots/            # App screenshots
├── services/
│   └── gemini_service.py   # Gemini AI integration
└── utils/
    ├── memory.py           # Chat history management
    └── resume_parser.py    # PDF text extraction
```

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open an issue for bugs or feature requests.

---

## 📬 Connect

[![GitHub](https://img.shields.io/badge/GitHub-aravindsai2202-181717?logo=github)](https://github.com/aravindsai2202)

---

<p align="center">⭐ <i>If you find this useful, give it a star!</i> ⭐</p>