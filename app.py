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
    "agentic ai",
    "aws",
    "azure",
    "vector database",
    "gcp",
    "rag"
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
    "llm": "LLM",

    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "rag": "RAG",
    "langchain": "LangChain",
    "generative ai": "Generative AI"
}

# =========================
# File Upload
# =========================
uploaded_file = st.file_uploader(
    "Choose a Resume PDF",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=200
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
        ats_score += 10
        st.success("✅ Contact Information Found")
    else:
        st.error("❌ Contact Information Missing")

    # Education
    if any(
        keyword in resume_text_lower
        for keyword in education_keywords
    ):
        ats_score += 10
        st.success("✅ Education Section Found")
    else:
        st.error("❌ Education Section Missing")

    # Skills
    if len(detected_skills) > 0:
        ats_score += 10
        st.success("✅ Skills Section Found")
    else:
        st.error("❌ Skills Section Missing")

    # Projects
    if any(
        keyword in resume_text_lower
        for keyword in project_keywords
    ):
        ats_score += 10
        st.success("✅ Projects Section Found")
    else:
        st.error("❌ Projects Section Missing")

    # LinkedIn / GitHub
    if any(
        keyword in resume_text_lower
        for keyword in linkedin_github_keywords
    ):
        ats_score += 10
        st.success("✅ LinkedIn / GitHub Found")
    else:
        st.error("❌ LinkedIn / GitHub Missing")

    # Skill Strength

    if len(detected_skills) >= 15:

        ats_score += 20
        st.success("✅ Strong Skill Set Detected")

    elif len(detected_skills) >= 10:

        ats_score += 15
        st.success("✅ Good Skill Set Detected")

    elif len(detected_skills) >= 5:

        ats_score += 10
        st.success("✅ Basic Skill Set Detected")

    else:

        st.warning("⚠ Few Skills Detected")

    # AI / ML Keywords

    ai_keywords = [

        "machine learning",
        "deep learning",
        "artificial intelligence",
        "nlp",
        "tensorflow",
        "pytorch",
        "rag",
        "llm",
        "generative ai"
    ]

    keyword_count = 0

    for keyword in ai_keywords:

        if keyword in resume_text_lower:

            keyword_count += 1

    ats_score += min(keyword_count * 2, 10)

    st.success(
        f"✅ AI Keywords Found: {keyword_count}"
    )        

    # Experience Check

    experience_keywords = [

        "intern",
        "experience",
        "work experience"
    ]

    if any(
        keyword in resume_text_lower
        for keyword in experience_keywords
    ):

        ats_score += 10

        st.success(
            "✅ Experience Section Found"
        )

    else:

        st.warning(
            "⚠ Experience Section Missing"
        )

    # Training / Certification

    training_keywords = [

        "certification",
        "training",
        "course"
    ]

    if any(
        keyword in resume_text_lower
        for keyword in training_keywords
    ):

        ats_score += 10

        st.success(
            "✅ Training / Certification Found"
        )

    else:

        st.warning(
            "⚠ Training / Certification Missing"
        )    

    # =========================
    # 7. ATS Score Meter
    # =========================

    ats_score = min(ats_score, 100)
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
    
    # ==========================
    # JOB MATCH ANALYSIS
    # ==========================

    st.subheader("🎯 Job Match Analysis")

    if job_description:

        # Convert Job Description to lowercase
        job_description_lower = job_description.lower()

        # Extract skills from Job Description
        job_skills = []

        for skill in skills_list:

            if skill in job_description_lower:
                job_skills.append(skill)

        # Find Matched Skills
        matched_skills = []

        for skill in job_skills:

            if skill in resume_text_lower:
                matched_skills.append(skill)

        # Find Missing Skills
        missing_skills = []

        for skill in job_skills:

            if skill not in resume_text_lower:
                missing_skills.append(skill)

        # Calculate Match Score
        if len(job_skills) > 0:

            match_score = int(
                (len(matched_skills) / len(job_skills)) * 100
            )

        else:
            match_score = 0

        # Display Match Score
        st.metric(
            "Job Match Score",
            f"{match_score}%"
        )

        st.progress(match_score / 100)

        # Display Matched Skills
        st.subheader("✅ Matched Skills")

        if matched_skills:

            for skill in matched_skills:
                if skill in skill_display_names:
                    st.write(f"✅ {skill_display_names[skill]}")
                else:
                    st.write(f"✅ {skill.title()}")
        else:
            st.warning("No matching skills found.")

        # Display Missing Skills
        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in missing_skills:
                if skill in skill_display_names:
                    st.write(f"❌ {skill_display_names[skill]}")
                else:
                    st.write(f"❌ {skill.title()}")
        else:
            st.success("No missing skills detected.")

    # ==========================
    # AI JOB MATCH FEEDBACK
    # ==========================

    st.subheader("🤖 AI Job Match Feedback")

    if job_description:

        if st.button("Generate Job Match Feedback"):

            with st.spinner("Analyzing Resume Against Job Description..."):

                model = genai.GenerativeModel("models/gemini-2.5-flash")

                prompt = f"""
                Compare the following Resume and Job Description.

                Analyze:

                1. Overall Match Percentage
                2. Strengths
                3. Missing Skills
                4. Interview Readiness
                5. Resume Improvement Suggestions
                6. Learning Roadmap

                Resume:

                {resume_text}

                Job Description:

                {job_description}
                """

                response = model.generate_content(prompt)

                st.markdown(response.text)