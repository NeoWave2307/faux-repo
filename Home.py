"""
CurricuLab AI - Intelligent Curriculum Design Platform
Production-grade minimalistic interface
"""
import streamlit as st
import os
from src.rag.vector_store import CurriculumVectorStore
from src.llm.client import GeminiClient
from src.curriculum.generator import CurriculumGenerator
from src.curriculum.validator import CurriculumValidator
from src.curriculum.models import CurriculumRequest
from src.pdf.generator import CurriculumPDFGenerator
from src.llm.career_prompts import get_career_path_prompt, get_course_recommendation_prompt
import json

# Page configuration
st.set_page_config(
    page_title="CurricuLab AI - Curriculum Design Platform",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ChatGPT-inspired minimalistic CSS
st.markdown("""
<style>
    /* Clean fonts and spacing */
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        background: #f7f7f8;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    
    /* Header */
    .app-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid #e5e5e5;
        margin-bottom: 2rem;
        background: white;
    }
    
    .app-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #202123;
        margin: 0;
    }
    
    .app-subtitle {
        font-size: 0.9rem;
        color: #6e6e80;
        margin-top: 0.25rem;
    }
    
    /* Role selector */
    .role-selector {
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .role-label {
        font-size: 0.875rem;
        color: #6e6e80;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        background: white;
        color: #202123;
        border: 1px solid #d9d9e3;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #f7f7f8;
        border-color: #c5c5d2;
    }
    
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #e5e5e5;
        background: white;
        padding: 0 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 0;
        color: #6e6e80;
        font-weight: 500;
        font-size: 0.875rem;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #202123;
        border-bottom-color: #202123;
    }
    
    /* Form elements */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div,
    .stNumberInput>div>div>input {
        border: 1px solid #d9d9e3;
        border-radius: 6px;
        padding: 0.75rem;
        font-size: 0.875rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #202123;
        box-shadow: 0 0 0 1px #202123;
    }
    
    /* Content cards */
    .content-card {
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Results section */
    .result-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #202123;
        margin-bottom: 1rem;
    }
    
    .metadata {
        color: #6e6e80;
        font-size: 0.875rem;
        line-height: 1.6;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: #10a37f;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        width: 100%;
    }
    
    .stDownloadButton>button:hover {
        background: #0d8c6f;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f7f7f8;
        border: 1px solid #e5e5e5;
        border-radius: 6px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'role' not in st.session_state:
    st.session_state['role'] = None

@st.cache_resource
def initialize_components():
    """Initialize AI components"""
    try:
        if not os.path.exists("./data/vector_db"):
            return None, "Knowledge base not initialized. Please run: python populate_knowledge_base.py"
        
        vector_store = CurriculumVectorStore()
        if vector_store.get_count() == 0:
            return None, "Knowledge base is empty. Please run: python populate_knowledge_base.py"
        
        llm_client = GeminiClient()
        generator = CurriculumGenerator(vector_store, llm_client)
        validator = CurriculumValidator()
        pdf_generator = CurriculumPDFGenerator()
        
        return (generator, validator, pdf_generator), None
    except ValueError as e:
        return None, f"Configuration error: {str(e)}"
    except Exception as e:
        return None, f"Initialization failed: {str(e)}"

# Header
st.markdown("""
<div class="app-header">
    <h1 class="app-title">CurricuLab AI</h1>
    <p class="app-subtitle">Intelligent Curriculum Design Platform</p>
</div>
""", unsafe_allow_html=True)

# Role Selection
if not st.session_state['role']:
    st.markdown('<div class="role-selector">', unsafe_allow_html=True)
    st.markdown('<p class="role-label">Select Your Role</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("Student", use_container_width=True):
            st.session_state['role'] = 'student'
            st.rerun()
    with col2:
        if st.button("Professor", use_container_width=True):
            st.session_state['role'] = 'professor'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Show selected role and allow change
col_role, col_change = st.columns([3, 1])
with col_role:
    st.caption(f"Current role: **{st.session_state['role'].title()}**")
with col_change:
    if st.button("Change Role", use_container_width=True):
        st.session_state['role'] = None
        st.rerun()

# Initialize components
result = initialize_components()
if result[1]:
    st.error(result[1])
    st.stop()

generator, validator, pdf_generator = result[0]

# Main Tabs
tab1, tab2, tab3 = st.tabs(["Curriculum Generator", "Career Path Planner", "Course Recommender"])

with tab1:
    st.markdown("### Generate Academic Curriculum")
    
    with st.form("curriculum_form"):
        skill = st.text_input("Subject/Skill Area", placeholder="e.g., Machine Learning, Data Science")
        
        col1, col2 = st.columns(2)
        with col1:
            level = st.selectbox("Education Level", ["BTech", "Masters", "Diploma", "Certification"])
        with col2:
            duration = st.number_input("Duration (Semesters)", min_value=1, max_value=12, value=4)
        
        specialization = st.text_input("Specialization (Optional)", placeholder="e.g., Deep Learning")
        focus_areas = st.text_area("Focus Areas (Optional, one per line)", placeholder="Neural Networks\nComputer Vision")
        
        use_rag = st.checkbox("Use AI context from knowledge base", value=True)
        
        submitted = st.form_submit_button("Generate Curriculum", use_container_width=True)
    
    if submitted and skill:
        focus_list = [area.strip() for area in focus_areas.split('\n') if area.strip()] if focus_areas else None
        
        request = CurriculumRequest(
            skill=skill,
            level=level,
            duration_semesters=duration,
            specialization=specialization if specialization else None,
            focus_areas=focus_list
        )
        
        with st.spinner("Generating curriculum..."):
            try:
                curriculum = generator.generate(request, use_rag=use_rag)
                st.session_state['curriculum'] = curriculum
                validation_report = validator.validate_and_report(curriculum)
                st.session_state['validation'] = validation_report
                st.success("Curriculum generated successfully")
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
    
    if 'curriculum' in st.session_state:
        curriculum = st.session_state['curriculum']
        
        st.markdown("---")
        st.markdown(f"### {curriculum.title}")
        st.markdown(f"<p class='metadata'><strong>Level:</strong> {curriculum.level} | <strong>Duration:</strong> {curriculum.duration_semesters} Semesters | <strong>Total Credits:</strong> {curriculum.total_credits}</p>", unsafe_allow_html=True)
        
        with st.expander("Overview", expanded=True):
            st.write(curriculum.overview)
        
        with st.expander("Semester Details"):
            for semester in curriculum.semesters:
                st.markdown(f"**Semester {semester.semester_number}** ({semester.total_credits} Credits)")
                for course in semester.courses:
                    st.markdown(f"- **{course.code}** - {course.name} ({course.credits} credits)")
                st.markdown("")
        
        with st.expander("Learning Outcomes"):
            for outcome in curriculum.learning_outcomes:
                st.markdown(f"- {outcome}")
        
        if curriculum.career_paths:
            with st.expander("Career Paths"):
                for career in curriculum.career_paths:
                    st.markdown(f"- {career}")
        
        # Download button
        try:
            pdf_buffer = pdf_generator.generate(curriculum)
            st.download_button(
                label="Download Curriculum PDF",
                data=pdf_buffer,
                file_name=f"{curriculum.title.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF generation failed: {str(e)}")

with tab2:
    st.markdown("### Career Path Planner")
    st.caption("Get a personalized learning curriculum aligned with your career goals")
    
    with st.form("career_form"):
        target_role = st.text_input("Target Career Role", placeholder="e.g., Machine Learning Engineer, Full Stack Developer")
        
        col1, col2 = st.columns(2)
        with col1:
            current_level = st.selectbox("Current Level", ["Beginner", "Intermediate", "Advanced", "Career Transition"])
        with col2:
            duration = st.number_input("Available Time (months)", min_value=3, max_value=24, value=12)
        
        background = st.text_area("Your Background (Optional)", placeholder="Current education, work experience, or skills")
        preferences = st.text_input("Learning Preferences (Optional)", placeholder="e.g., Hands-on projects, Theory-focused, Part-time friendly")
        
        career_submitted = st.form_submit_button("Generate Career Path", use_container_width=True)
    
    if career_submitted and target_role:
        pref_list = [p.strip() for p in preferences.split(',') if p.strip()] if preferences else None
        
        career_prompt = get_career_path_prompt(
            target_role=target_role,
            current_level=current_level,
            duration_months=duration,
            background=background if background else None,
            preferences=pref_list
        )
        
        with st.spinner(f"Creating personalized career path for {target_role}..."):
            try:
                # Generate using LLM
                llm_client = GeminiClient()
                response = llm_client.generate_with_retry(prompt=career_prompt, temperature=0.5)
                
                # Parse response
                json_str = response.strip()
                if "```json" in json_str:
                    json_str = json_str.split("```json")[1].split("```")[0].strip()
                elif "```" in json_str:
                    parts = json_str.split("```")
                    if len(parts) >= 2:
                        json_str = parts[1].strip()
                
                if "{" in json_str and "}" in json_str:
                    start = json_str.find("{")
                    end = json_str.rfind("}") + 1
                    json_str = json_str[start:end]
                
                from src.curriculum.models import Curriculum
                curriculum_data = json.loads(json_str)
                career_curriculum = Curriculum(**curriculum_data)
                
                st.session_state['career_curriculum'] = career_curriculum
                st.success(f"Career path to {target_role} generated successfully!")
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
    
    if 'career_curriculum' in st.session_state:
        curriculum = st.session_state['career_curriculum']
        
        st.markdown("---")
        st.markdown(f"### {curriculum.title}")
        st.markdown(f"<p class='metadata'><strong>Duration:</strong> {curriculum.duration_semesters} months | <strong>Total Learning Hours:</strong> {curriculum.total_credits * 10}+</p>", unsafe_allow_html=True)
        
        with st.expander("Learning Path Overview", expanded=True):
            st.write(curriculum.overview)
        
        with st.expander("Module Breakdown"):
            for semester in curriculum.semesters:
                st.markdown(f"**Module {semester.semester_number}**")
                for course in semester.courses:
                    st.markdown(f"- **{course.name}** ({course.category})")
                    st.caption(course.description)
                st.markdown("")
        
        with st.expander("Skills You'll Gain"):
            for outcome in curriculum.learning_outcomes:
                st.markdown(f"- {outcome}")
        
        if curriculum.career_paths:
            with st.expander("Career Opportunities"):
                for career in curriculum.career_paths:
                    st.markdown(f"- {career}")
        
        # Download
        try:
            pdf_buffer = pdf_generator.generate(curriculum)
            st.download_button(
                label="Download Career Path PDF",
                data=pdf_buffer,
                file_name=f"Career_Path_{target_role.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except:
            pass

with tab3:
    st.markdown("### Course Recommender")
    st.caption("Get personalized course recommendations based on your progress and interests")
    
    with st.form("recommender_form"):
        completed = st.text_area("Completed Courses (one per line)", placeholder="Introduction to Programming\nData Structures\nDatabase Systems")
        interests = st.text_input("Your Interests", placeholder="Machine Learning, Web Development, Cloud Computing")
        goal = st.text_input("Career Goal (Optional)", placeholder="e.g., Data Scientist")
        
        recommend_submitted = st.form_submit_button("Get Recommendations", use_container_width=True)
    
    if recommend_submitted and interests:
        completed_list = [c.strip() for c in completed.split('\n') if c.strip()]
        interest_list = [i.strip() for i in interests.split(',') if i.strip()]
        
        recommend_prompt = get_course_recommendation_prompt(
            completed_courses=completed_list,
            interests=interest_list,
            career_goal=goal if goal else None
        )
        
        with st.spinner("Analyzing your profile and generating recommendations..."):
            try:
                llm_client = GeminiClient()
                response = llm_client.generate_with_retry(prompt=recommend_prompt, temperature=0.6)
                
                # Parse JSON array
                json_str = response.strip()
                if "```json" in json_str:
                    json_str = json_str.split("```json")[1].split("```")[0].strip()
                elif "```" in json_str:
                    parts = json_str.split("```")
                    if len(parts) >= 2:
                        json_str = parts[1].strip()
                
                if "[" in json_str and "]" in json_str:
                    start = json_str.find("[")
                    end = json_str.rfind("]") + 1
                    json_str = json_str[start:end]
                
                recommendations = json.loads(json_str)
                st.session_state['recommendations'] = recommendations
                st.success(f"Found {len(recommendations)} recommended courses!")
            except Exception as e:
                st.error(f"Recommendation failed: {str(e)}")
    
    if 'recommendations' in st.session_state:
        st.markdown("---")
        st.markdown("### Recommended Courses")
        
        for i, rec in enumerate(st.session_state['recommendations'], 1):
            with st.expander(f"{i}. {rec.get('name', 'Course')}", expanded=i <= 3):
                st.markdown(f"**Code:** {rec.get('code', 'N/A')}")
                st.markdown(f"**Credits:** {rec.get('credits', 'N/A')}")
                st.markdown(f"**Category:** {rec.get('category', 'N/A')}")
                st.markdown(f"**Why recommended:** {rec.get('reason', 'No reason provided')}")
