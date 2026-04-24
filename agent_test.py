# from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
# from autogen_ext.models.openai import OpenAIChatCompletionClient
# from autogen_agentchat.teams import RoundRobinGroupChat
# from dotenv import load_dotenv
# from autogen_agentchat.conditions import TextMentionTermination
# from autogen_agentchat.base import TaskResult
# import os

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key=OPENAI_API_KEY)


# print("Fuck YOU..........<<<.......>>>")
# async def my_agents(job_position = "AI Engineer"):
#     interviewer = AssistantAgent(
#         name = "Interviewer",
#         model_client= model_client,
#         description=f"An AI agent that conducts interviews for a {job_position} position.",
#         system_message=f'''
#         You are a professional interviewer for a {job_position} position.
#         Ask one clear question at a time and Wait for user to respond. 
#         Your job. is to continue and ask questions, don't pay any attention to career coach response. 
#         Make sure to ask question based on Candidate's answer and your expertise in the field.
#         Ask 3 questions in total covering technical skills and experience, problem-solving abilities, and cultural fit.
#         After asking 3 questions, say 'TERMINATE' at the end of the interview.
#         Make question under 50 words.
#     '''
#     )

    
#     candidate = UserProxyAgent(
#         name= "Candidate",
#         description=f"An agent that simulates a candidate for a {job_position} position.",
#         input_func=input
#     )


#     evaluation = AssistantAgent(
#         name = "Evaluator",
#         model_client= model_client,
#         description=f"An AI agent that provides feedback and advice to candidates for a {job_position} position.",
#         system_message=f'''
#         You are a career coach specializing in preparing candidates for {job_position} interviews.
#         Provide constructive feedback on the candidate's responses and suggest improvements.
#         After the interview, summarize the candidate's performance and provide actionable advice.
#         Make it under 100 words.
#     '''

#     )

#     terninate_condition = TextMentionTermination(text="TERMINATE")

#     team = RoundRobinGroupChat(
#         participants=[interviewer, candidate, evaluation],
#         termination_condition= terninate_condition,
#         max_turns=20
#     )

#     return team



# async def run_interview(team):
#     async for message in team.run_stream(task='Start the interview with the first question ?'):

#         if isinstance(message, TaskResult):
#             message = f'Interview completed with result: {message.stop_reason}'
#             yield message
        
#         else:
#             message = f'{message.source}: {message.content}'
#             yield message



# async def main():
#     job_position = "AI Engineer"
#     team = await my_agents(job_position)

#     async for message in run_interview(team):
#         print('-' * 70)
#         print(message)




# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())





# ======================






# ==============================
# 🔑 DIRECT API KEY (NO .env)
# ==============================
# GEMINI_API_KEY = "AIzaSyDLJLTUBuDHKPfTXPSD51spjlxiN5Jhpxc"

# import asyncio
# from google import genai

# # =========================
# # 🔥 CONFIG
# # =========================
# API_KEY = ""
# MODEL = "gemini-2.5-flash"

# if not API_KEY or "YOUR_NEW" in API_KEY:
#     raise ValueError("❌ Please add your Gemini API key")

# # =========================
# # 🔥 GEMINI CLIENT
# # =========================
# class GeminiClient:
#     def __init__(self, api_key, model=MODEL):
#         self.client = genai.Client(api_key=api_key)
#         self.model = model

#         self.model_info = {
#             "vision": False,
#             "function_calling": True,
#             "json_output": False,
#         }

#     async def create(self, messages):

#         prompt = ""
#         for m in messages:
#             role = getattr(m, "role", "user")
#             content = getattr(m, "content", "")
#             prompt += f"{role}: {content}\n"

#         response = self.client.models.generate_content(
#             model=self.model,
#             contents=prompt
#         )

#         class Result:
#             def __init__(self, text):
#                 self.content = text

#         return Result(response.text)


# # =========================
# # 🔥 SIMPLE SCORING ENGINE
# # =========================
# def score_answer(answer: str):
#     score = {
#         "communication": 0,
#         "technical": 0,
#         "clarity": 0
#     }

#     length = len(answer.split())

#     # Communication
#     if length > 30:
#         score["communication"] = 8
#     elif length > 15:
#         score["communication"] = 6
#     else:
#         score["communication"] = 4

#     # Technical keyword detection
#     keywords = ["python", "ml", "ai", "data", "model", "algorithm"]
#     tech_hits = sum(1 for k in keywords if k in answer.lower())

#     score["technical"] = min(10, tech_hits * 2)

#     # Clarity
#     if "." in answer:
#         score["clarity"] = 7
#     else:
#         score["clarity"] = 5

#     return score


# # =========================
# # 🔥 INTERVIEW SYSTEM
# # =========================
# async def run_interview():

#     llm = GeminiClient(API_KEY)

#     messages = [
#         type("msg", (), {
#             "role": "system",
#             "content": "You are a strict but fair AI interviewer. Ask one question at a time."
#         })()
#     ]

#     print("\n🚀 EVALUAHIRE AI INTERVIEW STARTED\n")

#     total_scores = []

#     # Initial question
#     messages.append(type("msg", (), {
#         "role": "user",
#         "content": "Start interview. Ask first question."
#     })())

#     for i in range(5):  # 5 questions

#         ai = await llm.create(messages)

#         print(f"\n🤖 AI: {ai.content}")

#         user = input("\n👤 You: ")

#         # scoring
#         score = score_answer(user)
#         total_scores.append(score)

#         print(f"\n📊 Score: {score}")

#         # update memory
#         messages.append(type("msg", (), {
#             "role": "assistant",
#             "content": ai.content
#         })())

#         messages.append(type("msg", (), {
#             "role": "user",
#             "content": user
#         })())

#     # =========================
#     # FINAL REPORT
#     # =========================
#     print("\n============================")
#     print("🏁 FINAL INTERVIEW REPORT")
#     print("============================")

#     avg_comm = sum(s["communication"] for s in total_scores) / len(total_scores)
#     avg_tech = sum(s["technical"] for s in total_scores) / len(total_scores)
#     avg_clarity = sum(s["clarity"] for s in total_scores) / len(total_scores)

#     print(f"Communication: {avg_comm:.2f}/10")
#     print(f"Technical: {avg_tech:.2f}/10")
#     print(f"Clarity: {avg_clarity:.2f}/10")

#     final_score = (avg_comm + avg_tech + avg_clarity) / 3

#     print(f"\n⭐ FINAL SCORE: {final_score:.2f}/10")

#     if final_score > 7:
#         print("✅ Status: Strong Candidate")
#     elif final_score > 5:
#         print("⚠️ Status: Average Candidate")
#     else:
#         print("❌ Status: Needs Improvement")


# # =========================
# # RUN
# # =========================
# if __name__ == "__main__":
#     asyncio.run(run_interview())


# GEMINI_API_KEY = "AIzaSyDLJLTUBuDHKPfTXPSD51spjlxiN5Jhpxc"

import asyncio
from google import genai

# =========================
# 🔑 CONFIG
# =========================
API_KEY = "AIzaSyDLJLTUBuDHKPfTXPSD51spjlxiN5Jhpxc"
MODEL = "gemini-2.5-flash"

client = genai.Client(api_key=API_KEY)


# =========================
# 🤖 GEMINI WRAPPER
# =========================
class GeminiLLM:
    def __init__(self, system_prompt=""):
        self.system_prompt = system_prompt

    async def ask(self, prompt):

        full_prompt = f"""
System: {self.system_prompt}

User: {prompt}
"""

        response = client.models.generate_content(
            model=MODEL,
            contents=full_prompt
        )

        return response.text


# =========================
# 🎯 SCORING ENGINE
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
# 🤖 AGENTS (INTERVIEW SYSTEM)
# =========================
async def run_interview(job_position="AI Engineer"):

    interviewer = GeminiLLM(
        system_prompt=f"""
You are a professional interviewer for {job_position}.

Rules:
- Ask ONE question at a time
- Total 3 questions only
- Cover:
  1. Technical skills
  2. Problem solving
  3. Cultural fit

After 3 questions say: TERMINATE
Keep questions short.
"""
    )

    evaluator = GeminiLLM(
        system_prompt=f"""
You are a strict evaluator for {job_position}.
Give short feedback and improvement suggestions.
Max 80 words.
"""
    )

    print("\n🚀 INTERVIEW STARTED (GEMINI SYSTEM)\n")

    scores = []

    for i in range(3):

        # =========================
        # INTERVIEWER QUESTION
        # =========================
        question = await interviewer.ask(
            f"Ask question {i+1} for {job_position} interview"
        )

        print(f"\n🤖 Interviewer: {question}")
        print("====================================")

        # =========================
        # CANDIDATE ANSWER
        # =========================
        answer = input("\n👤 Candidate: ")

        # =========================
        # SCORING
        # =========================
        s = score_answer(answer)
        scores.append(s)

        print(f"\n📊 Score: {s}")
        print("====================================")

        # =========================
        # EVALUATOR FEEDBACK
        # =========================
        feedback = await evaluator.ask(
            f"""
Question: {question}
Answer: {answer}

Give feedback and improvement tips.
"""
        )

        print(f"\n🧠 Evaluator: {feedback}")
        print("====================================")

    # =========================
    # FINAL REPORT
    # =========================
    print("\n========================")
    print("🏁 FINAL REPORT")
    print("========================")

    avg_comm = sum(s["communication"] for s in scores) / 3
    avg_tech = sum(s["technical"] for s in scores) / 3
    avg_clarity = sum(s["clarity"] for s in scores) / 3

    final_score = (avg_comm + avg_tech + avg_clarity) / 3

    # print(f"Communication: {avg_comm:.2f}/10")
    # print(f"Technical: {avg_tech:.2f}/10")
    # print(f"Clarity: {avg_clarity:.2f}/10")
    print(f"\n⭐ FINAL SCORE: {final_score:.2f}/10")

    if final_score > 7:
        print("✅ Strong Candidate")
    elif final_score > 5:
        print("⚠️ Average Candidate")
    else:
        print("❌ Needs Improvement")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    asyncio.run(run_interview())