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

    progress = st.progress(0)
    stage_box = st.container()

    try:
        # Stage 1: Understand and plan
        with stage_box:
            st.markdown('<div class="stage"><div class="stage-title">Stage 1 — Understanding the topic</div></div>', unsafe_allow_html=True)
            with st.spinner("AI is identifying the important concepts..."):
                stage1 = generate_stage(
                    build_stage_1_prompt(subject, topic, level)
                )
            st.write(stage1)
        progress.progress(20)

        # Stage 2: Notes
       with st.spinner("AI is creating structured notes..."):
    stage2_prompt = build_stage_2_prompt(
        subject, topic, level, stage1
    )

    st.write("Stage 2 prompt characters:", len(stage2_prompt))

    stage2 = generate_stage(stage2_prompt)

st.write(stage2)
        progress.progress(40)

        # Stage 3: Key questions
        with stage_box:
            st.markdown('<div class="stage"><div class="stage-title">Stage 3 — Generating important questions</div></div>', unsafe_allow_html=True)
            with st.spinner("AI is preparing exam-focused questions..."):
                stage3 = generate_stage(
                    build_stage_3_prompt(subject, topic, stage2)
                )
            st.write(stage3)
        progress.progress(60)

        # Stage 4: Quiz
        with stage_box:
            st.markdown('<div class="stage"><div class="stage-title">Stage 4 — Creating the quiz</div></div>', unsafe_allow_html=True)
            with st.spinner("AI is creating the quiz..."):
                stage4 = generate_stage(
                    build_stage_4_prompt(subject, topic, stage2, question_count)
                )
            st.write(stage4)
        progress.progress(80)

        # Stage 5: Final study plan
        with stage_box:
            st.markdown('<div class="stage"><div class="stage-title">Stage 5 — Building the final study pack</div></div>', unsafe_allow_html=True)
            with st.spinner("AI is combining the results into the final study pack..."):
                stage5 = generate_stage(
                    build_stage_5_prompt(subject, topic, level, stage1, stage2, stage3, stage4)
                )
            st.write(stage5)
        progress.progress(100)

        st.success("✅ Study pack completed!")

    except Exception as e:
        st.error("The AI request failed. Check your API key and terminal/deployment logs.")
        st.exception(e)
