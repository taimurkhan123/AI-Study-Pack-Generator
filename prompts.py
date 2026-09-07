def build_stage_1_prompt(subject, topic, level):
    return f"""
You are a study-planning expert.

Subject: {subject}
Topic: {topic}
Student level: {level}

Analyze the topic for a student. Identify:
1. What the topic means.
2. The most important concepts.
3. Prerequisites the student should know.
4. The best learning order.

Do not write the final study notes yet. Return a concise learning blueprint.
""".strip()


def build_stage_2_prompt(subject, topic, level, blueprint):
    return f"""
You are an expert teacher.

Create clear study notes for:
Subject: {subject}
Topic: {topic}
Student level: {level}

Use this blueprint from Stage 1:
--- BEGIN STAGE 1 ---
{blueprint}
--- END STAGE 1 ---

Explain each important concept in simple language.
Use headings, bullet points, examples, and short definitions.
Do not invent facts. Keep the notes focused on the topic.
""".strip()


def build_stage_3_prompt(subject, topic, notes):
    return f"""
You are an exam-preparation teacher.

Create important exam questions for:
Subject: {subject}
Topic: {topic}

Use these notes from Stage 2:
--- BEGIN STAGE 2 ---
{notes}
--- END STAGE 2 ---

Create a balanced set of questions:
- short-answer questions
- conceptual questions
- application/problem-solving questions

Give a short answer key after the questions.
""".strip()


def build_stage_4_prompt(subject, topic, notes, question_count):
    return f"""
You are a quiz designer.

Create a {question_count}-question quiz for:
Subject: {subject}
Topic: {topic}

Use the study notes from Stage 2:
--- BEGIN STAGE 2 ---
{notes}
--- END STAGE 2 ---

Requirements:
- Mix easy, medium, and difficult questions.
- Prefer multiple-choice questions.
- Give 4 options for each question.
- Put the answer key at the end.
- Do not add explanations to the answer key yet.
""".strip()


def build_stage_5_prompt(subject, topic, level, blueprint, notes, questions, quiz):
    return f"""
You are the final study-pack editor.

Build a complete, student-friendly study pack for:
Subject: {subject}
Topic: {topic}
Level: {level}

Combine the outputs from all previous stages.

STAGE 1 — BLUEPRINT
{blueprint}

STAGE 2 — NOTES
{notes}

STAGE 3 — IMPORTANT QUESTIONS
{questions}

STAGE 4 — QUIZ
{quiz}

Return the final pack with this structure:

# {topic} — Study Pack

## 1. Learning Objectives
## 2. Quick Revision
## 3. Detailed Notes
## 4. Important Questions
## 5. Quiz
## 6. Answer Key
## 7. One-Day Revision Plan

Make the final answer clear and useful for a student.
Do not mention that you are an AI or describe the internal prompt chain.
""".strip()
