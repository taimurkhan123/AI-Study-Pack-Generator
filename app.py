import streamlit as st
from ai_service import generate_stage
from prompts import (
    build_stage_1_prompt,
    build_stage_2_prompt,
    build_stage_3_prompt,
    build_stage_4_prompt,
    build_stage_5_prompt,
)

st.set_page_config(
    page_title="AI Study Pack Generator",
    page_icon="📚",
    layout="wide",
)

st.markdown("""
<style>
.stage {
    border-left: 4px solid #2563eb;
    padding: 0.35rem 0 0.35rem 1rem;
    margin: 0.75rem 0;
}
.stage-title {
    color: #2563eb;
    font-weight: 700;
    font-size: 1.05rem;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 AI Study Pack Generator")
st.caption("A practical prompt-chaining project using Python, Streamlit, and Gemini 3.6 Flash.")

# Initialize session state storage for stages
if "study_pack_data" not in st.session_state:
    st.session_state.study_pack_data = {}

with st.sidebar:
    st.header("Study Settings")
    subject = st.text_input("Subject", "Computer Networks")
    topic = st.text_input("Topic", "OSI Model")
    level = st.selectbox("Student Level", ["Beginner", "Intermediate", "Advanced"])
    question_count = st.slider("Quiz Questions", 5, 15, 10)

st.write("Enter a topic and generate a complete study pack through five AI stages.")

if st.button("🚀 Generate Study Pack", type="primary"):
    if not subject.strip() or not topic.strip():
        st.warning("Please enter both a subject and a topic.")
        st.stop()

    st.session_state.study_pack_data = {}
    progress = st.progress(0)

    try:
        # Stage 1: Understand and plan
        with st.status("Stage 1: Identifying key concepts...", expanded=True) as status:
            stage1 = generate_stage(build_stage_1_prompt(subject, topic, level))
            st.session_state.study_pack_data["stage1"] = stage1
            status.update(label="Stage 1 Complete!", state="complete", expanded=False)
        progress.progress(20)

        # Stage 2: Notes
        with st.status("Stage 2: Creating study notes...", expanded=True) as status:
            stage2 = generate_stage(build_stage_2_prompt(subject, topic, level, st.session_state.study_pack_data["stage1"]))
            st.session_state.study_pack_data["stage2"] = stage2
            status.update(label="Stage 2 Complete!", state="complete", expanded=False)
        progress.progress(40)

        # Stage 3: Key questions
        with st.status("Stage 3: Preparing exam-focused questions...", expanded=True) as status:
            stage3 = generate_stage(build_stage_3_prompt(subject, topic, st.session_state.study_pack_data["stage2"]))
            st.session_state.study_pack_data["stage3"] = stage3
            status.update(label="Stage 3 Complete!", state="complete", expanded=False)
        progress.progress(60)

        # Stage 4: Quiz
        with st.status("Stage 4: Creating quiz...", expanded=True) as status:
            stage4 = generate_stage(build_stage_4_prompt(subject, topic, st.session_state.study_pack_data["stage2"], question_count))
            st.session_state.study_pack_data["stage4"] = stage4
            status.update(label="Stage 4 Complete!", state="complete", expanded=False)
        progress.progress(80)

        # Stage 5: Final study plan
        with st.status("Stage 5: Compiling final study pack...", expanded=True) as status:
            stage5 = generate_stage(
                build_stage_5_prompt(
                    subject,
                    topic,
                    level,
                    st.session_state.study_pack_data["stage1"],
                    st.session_state.study_pack_data["stage2"],
                    st.session_state.study_pack_data["stage3"],
                    st.session_state.study_pack_data["stage4"]
                )
            )
            st.session_state.study_pack_data["stage5"] = stage5
            status.update(label="Stage 5 Complete!", state="complete", expanded=False)
        progress.progress(100)

        st.success("✅ Study pack completed!")

    except Exception as e:
        st.error("The AI request failed. Check your API key and Cloud logs.")
        st.exception(e)

# Display results safely from session state
if "stage5" in st.session_state.study_pack_data:
    st.divider()
    st.markdown(st.session_state.study_pack_data["stage5"])
