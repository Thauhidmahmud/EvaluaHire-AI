
import asyncio
import streamlit as st
from google import genai

# =========================
# CONFIG
# =========================
API_KEY = "AIzaSyDLJLTUBuDHKPfTXPSD51spjlxiN5Jhpxc"
MODEL = "gemini-2.5-flash"

client = genai.Client(api_key=API_KEY)


# =========================
# SESSION STATE INIT
# =========================
def init_state():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "chat" not in st.session_state:
        st.session_state.chat = []
    if "scores" not in st.session_state:
        st.session_state.scores = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = None


init_state()


# =========================
# GEMINI WRAPPER
# =========================
class GeminiLLM:
    def __init__(self, system_prompt=""):
        self.system_prompt = system_prompt

    async def ask(self, prompt):
        response = client.models.generate_content(
            model=MODEL,
            contents=f"{self.system_prompt}\n\nUser: {prompt}"
        )
        return response.text


# =========================
# SIMPLE SCORING
# =========================
def score_answer(text):
    keywords = ["python", "ai", "ml", "model", "data", "algorithm"]
    tech = sum(1 for k in keywords if k in text.lower())

    return {
        "communication": min(10, len(text.split()) // 5),
        "technical": min(10, tech * 2),
        "clarity": 8 if "." in text else 6
    }


# =========================
# UI SETUP
# =========================
st.set_page_config(page_title="EvaluaHire", layout="wide")

st.title("🚀 EvaluaHire AI Interview System")
st.caption("AI-powered Interview + Evaluation System")

job_position = st.text_input("💼 Job Position", "AI Engineer")


# =========================
# START BUTTON (FIXED)
# =========================
if st.button("▶ Start Interview", key="start"):

    st.session_state.started = True
    st.session_state.step = 0
    st.session_state.chat = []
    st.session_state.scores = []
    st.session_state.current_question = None

    st.rerun()


# =========================
# BLOCK UNTIL START
# =========================
if not st.session_state.started:
    st.info("👆 Click Start Interview to begin")
    st.stop()


# =========================
# LLM SETUP
# =========================
interviewer = GeminiLLM(
    system_prompt=f"You are an interviewer for {job_position}. Ask ONE question. Total 3 questions."
)

evaluator = GeminiLLM(
    system_prompt=f"You are a strict evaluator for {job_position}. Give short feedback under 80 words."
)


# =========================
# CONTROL PANEL
# =========================
st.divider()

col1, col2 = st.columns(2)

with col1:
    ask_btn = st.button("❓ Ask Next Question", use_container_width=True)

with col2:
    st.metric("Progress", f"{st.session_state.step}/3")


# =========================
# ASK QUESTION
# =========================
if ask_btn and st.session_state.step < 3:

    async def get_question():
        return await interviewer.ask(
            f"Ask question {st.session_state.step + 1}"
        )

    question = asyncio.run(get_question())

    st.session_state.chat.append(("🤖 Interviewer", question))
    st.session_state.current_question = question
    st.session_state.step += 1


# =========================
# ANSWER SECTION
# =========================
if st.session_state.current_question:

    st.subheader("📝 Your Answer")

    answer = st.text_area("Type your answer here...", height=120)

    submit = st.button("✅ Submit Answer", use_container_width=True)

    if submit and answer:

        # save answer
        st.session_state.chat.append(("👤 You", answer))

        # score
        score = score_answer(answer)
        st.session_state.scores.append(score)

        st.session_state.chat.append(("📊 Score", str(score)))

        # feedback
        async def get_feedback():
            return await evaluator.ask(
                f"Q: {st.session_state.current_question}\nA: {answer}"
            )

        feedback = asyncio.run(get_feedback())

        st.session_state.chat.append(("🧠 Evaluator", feedback))

        st.session_state.current_question = None


# =========================
# CHAT DISPLAY
# =========================
st.divider()
st.subheader("💬 Interview Conversation")

for role, msg in st.session_state.chat:

    if role == "🤖 Interviewer":
        st.success(f"{role}: {msg}")

    elif role == "👤 You":
        st.info(f"{role}: {msg}")

    elif role == "📊 Score":
        st.warning(f"{role}: {msg}")

    else:
        st.write(f"**{role}:** {msg}")


# =========================
# FINAL RESULT
# =========================
if st.session_state.step >= 3 and st.session_state.scores:

    st.divider()
    st.subheader("🏁 Final Report")

    avg_comm = sum(s["communication"] for s in st.session_state.scores) / 3
    avg_tech = sum(s["technical"] for s in st.session_state.scores) / 3
    avg_clarity = sum(s["clarity"] for s in st.session_state.scores) / 3

    final = (avg_comm + avg_tech + avg_clarity) / 3

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Communication", f"{avg_comm:.2f}")
    col2.metric("Technical", f"{avg_tech:.2f}")
    col3.metric("Clarity", f"{avg_clarity:.2f}")
    col4.metric("Final Score", f"{final:.2f}/10")

    if final > 7:
        st.success("✅ Strong Candidate")
    elif final > 5:
        st.warning("⚠️ Average Candidate")
    else:
        st.error("❌ Needs Improvement")