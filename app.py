import streamlit as st
import pdfplumber
import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# =========================
# Title
# =========================
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume for analysis.")

# =========================
# Skills Database
# =========================
skills_list = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "tensorflow",
    "pytorch",
    "opencv",
    "streamlit",
    "pandas",
    "numpy",
    "scikit-learn",
    "power bi",
    "excel",
    "git",
    "github",
    "docker",
    "flask",
    "fastapi",
    "langchain",
    "generative ai",
    "llm",
    "agentic ai"
]

# =========================
# Display Names
# =========================
skill_display_names = {
    "sql": "SQL",
    "opencv": "OpenCV",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-Learn",
    "github": "GitHub",
    "power bi": "Power BI",
    "nlp": "NLP",
    "llm": "LLM"
}

# =========================
# File Upload
# =========================
uploaded_file = st.file_uploader(
    "Choose a Resume PDF",
    type=["pdf"]
)

# =========================
# Resume Processing
# =========================
if uploaded_file is not None:

    st.success("Resume uploaded successfully!")
    st.write("**File Name:**", uploaded_file.name)

    # =========================
    # 1. Extract Resume Text
    # =========================

    resume_text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:

            text = page.extract_text()

            if text:
                resume_text += text + "\n"

    # =========================
    # Display Extracted Text
    # =========================

    st.subheader("📄 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=250
    )

    # =========================
    # 2. Detect Skills
    # =========================

    resume_text_lower = resume_text.lower()

    detected_skills = []

    for skill in skills_list:

        if skill in resume_text_lower:

            if skill in skill_display_names:
                detected_skills.append(
                    skill_display_names[skill]
                )
            else:
                detected_skills.append(
                    skill.title()
                )

    # =========================
    # 3. Remove Duplicates
    # =========================

    detected_skills = list(set(detected_skills))

    # =========================
    # 4. Sort Skills
    # =========================

    detected_skills.sort()

    # =========================
    # 5. Display Skills
    # =========================

    st.subheader("🛠 Detected Skills")

    if detected_skills:

        for skill in detected_skills:
            st.markdown(f"✅ {skill}")

    else:
        st.warning("No skills detected.")

    # =========================
    # 6. ATS Score Analysis
    # =========================

    ats_score = 0

    contact_keywords = [
        "@",
        "phone",
        "+91"
    ]

    education_keywords = [
        "education",
        "bachelor",
        "degree",
        "cgpa"
    ]

    project_keywords = [
        "project",
        "projects"
    ]

    linkedin_github_keywords = [
        "linkedin",
        "github"
    ]

    st.subheader("📊 ATS Score Analysis")

    # Contact Information
    if any(
        keyword in resume_text_lower
        for keyword in contact_keywords
    ):
        ats_score += 20
        st.success("✅ Contact Information Found")
    else:
        st.error("❌ Contact Information Missing")

    # Education
    if any(
        keyword in resume_text_lower
        for keyword in education_keywords
    ):
        ats_score += 20
        st.success("✅ Education Section Found")
    else:
        st.error("❌ Education Section Missing")

    # Skills
    if len(detected_skills) > 0:
        ats_score += 20
        st.success("✅ Skills Section Found")
    else:
        st.error("❌ Skills Section Missing")

    # Projects
    if any(
        keyword in resume_text_lower
        for keyword in project_keywords
    ):
        ats_score += 20
        st.success("✅ Projects Section Found")
    else:
        st.error("❌ Projects Section Missing")

    # LinkedIn / GitHub
    if any(
        keyword in resume_text_lower
        for keyword in linkedin_github_keywords
    ):
        ats_score += 20
        st.success("✅ LinkedIn / GitHub Found")
    else:
        st.error("❌ LinkedIn / GitHub Missing")

    # =========================
    # 7. ATS Score Meter
    # =========================

    st.subheader("🎯 ATS Score")

    st.metric(
        label="ATS Score",
        value=f"{ats_score}/100"
    )

    st.progress(
        ats_score / 100
    )

    # =========================
    # AI Resume Feedback
    # =========================

    st.subheader("🤖 AI Resume Feedback")

    if st.button("Generate AI Feedback"):

        with st.spinner("Analyzing Resume..."):

            model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            prompt = f"""
            Analyze the following resume.

            Provide:

            1. Professional Resume Summary
            2. Key Strengths
            3. Weaknesses or Missing Areas
            4. ATS Improvement Suggestions
            5. Recommended Skills to Learn

            Resume:

            {resume_text}
            """

            try:

                response = model.generate_content(
                prompt
            )

                st.write(response.text)

            except Exception as e:

                st.error(f"Error: {e}")
