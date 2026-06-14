import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def generate_response(query, history):
    messages = [{
        "role": "system",
        "content": (
            "You are Career Copilot, an expert AI career advisor. "
            "You help users with career guidance, job searching, interview preparation, "
            "skill development, resume tips, and career roadmaps. "
            "Be concise, practical, and encouraging."
        )
    }]
    for msg in history[:-1]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model=MODEL, messages=messages, max_tokens=1024, temperature=0.7
    )
    return response.choices[0].message.content


def analyze_resume(resume_text):
    prompt = f"""You are an expert resume reviewer and career coach.
Analyze the following resume thoroughly and provide structured feedback.

RESUME:
{resume_text}

Provide your analysis in this exact format:

## ✅ Strengths
- List key strengths of the resume

## ⚠️ Weaknesses
- List areas that need improvement

## 🎯 Missing Skills
- List important skills that are absent

## 📊 ATS Score
Give a score out of 100 and explain why

## 💡 Suggestions
- List specific actionable improvements
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048, temperature=0.5
    )
    return response.choices[0].message.content


def generate_roadmap(current_role, target_role, experience):
    prompt = f"""You are a career strategist. Create a detailed career roadmap.

Current Role: {current_role}
Target Role: {target_role}
Years of Experience: {experience}

Provide a structured roadmap in this format:

## 🗺️ Career Roadmap: {current_role} → {target_role}

## 📍 Where You Are Now
Brief assessment of current position

## 🎯 Goal Overview
What it takes to become a {target_role}

## 📅 Phase 1 (0–3 months): Foundation
- Skills to learn
- Certifications to get
- Actions to take

## 📅 Phase 2 (3–6 months): Building
- Skills to learn
- Projects to build
- Actions to take

## 📅 Phase 3 (6–12 months): Launch
- Skills to learn
- Job search strategy
- Actions to take

## 🛠️ Key Tools & Technologies
List the most important ones

## 📚 Top Resources
Courses, books, communities
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048, temperature=0.6
    )
    return response.choices[0].message.content


def match_job_description(resume_text, job_description):
    prompt = f"""You are an expert recruiter and career coach.
Compare this resume against the job description and provide a detailed match analysis.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide analysis in this format:

## 🎯 Match Score
Give a percentage score and brief explanation

## ✅ Matching Skills & Keywords
List skills/keywords found in both resume and JD

## ❌ Missing Keywords
List important JD keywords missing from resume

## 📝 Resume Tweaks
Specific changes to tailor resume for this role

## 💬 Cover Letter Angle
Key points to highlight in a cover letter

## 🏆 Interview Focus Areas
Topics to prepare based on this JD
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048, temperature=0.5
    )
    return response.choices[0].message.content


def generate_interview_questions(role, experience_level, interview_type):
    prompt = f"""You are an expert interviewer. Generate realistic interview questions and ideal answers.

Role: {role}
Experience Level: {experience_level}
Interview Type: {interview_type}

Provide in this format:

## 🎤 Interview Prep: {role} ({interview_type})

## 🔥 Top 5 Questions You'll Definitely Be Asked
For each question:
**Q: [Question]**
💡 Ideal Answer: [Detailed answer with tips]

## 🧠 5 Tricky Questions to Watch Out For
For each question:
**Q: [Question]**
💡 How to Handle It: [Strategy and sample answer]

## ❓ 5 Questions YOU Should Ask the Interviewer
List smart questions that impress interviewers

## 🏆 Key Tips for This Interview Type
Specific advice for {interview_type} interviews
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048, temperature=0.7
    )
    return response.choices[0].message.content


def analyze_skill_gap(current_skills, target_role, experience_level):
    prompt = f"""You are a skills assessment expert and career coach.
Analyze the skill gap between current skills and target role requirements.

Current Skills: {current_skills}
Target Role: {target_role}
Experience Level: {experience_level}

Provide analysis in this format:

## 📊 Skill Gap Analysis: {target_role}

## ✅ Skills You Already Have
List matching skills with proficiency assessment

## 🚨 Critical Missing Skills
Skills that are must-have for this role (learn first)

## ⚠️ Nice-to-Have Skills
Skills that will make you stand out

## 📚 Learning Plan
### Week 1–4:
### Month 2–3:
### Month 4–6:

## 🎓 Recommended Certifications
List the most valuable ones with links/platforms

## ⏱️ Estimated Time to Be Job-Ready
Realistic timeline with current skill set
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048, temperature=0.6
    )
    return response.choices[0].message.content


def save_chat_history(history):
    import json
    from datetime import datetime
    filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(history, f, indent=2)
    return filename