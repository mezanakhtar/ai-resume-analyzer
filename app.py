import streamlit as st
import pdfplumber

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

    # Extract Text
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
    # Skill Detection
    # =========================
    resume_text_lower = resume_text.lower()

    detected_skills = []

    for skill in skills_list:

        if skill in resume_text_lower:

            if skill in skill_display_names:
                detected_skills.append(skill_display_names[skill])
            else:
                detected_skills.append(skill.title())

    # Remove Duplicates
    detected_skills = list(set(detected_skills))

    # Sort Alphabetically
    detected_skills.sort()

    # =========================
    # Display Skills
    # =========================
    st.subheader("🛠 Detected Skills")

    if detected_skills:

        for skill in detected_skills:
            st.markdown(f"✅ {skill}")

    else:
        st.warning("No skills detected.")