from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from supabase import create_client
import json
import os
from dotenv import load_dotenv


def load_environment():
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    return {
        "supabase_url": os.getenv("SUPABASE_URL"),
        "supabase_key": os.getenv("SUPABASE_KEY"),
    }


def get_big_five_chain() -> RunnableSequence:
    prompt = PromptTemplate(
        input_variables=["transcript"],
        template="""
You are a psychologist analyzing feedback about a person.

You are given a transcript of a feedback call about this person.

Based on it infer the person’s Big Five personality traits.

Rate each trait from 0 to 100, and explain briefly why you gave each rating.

Also please include a prediction of their IQ and EQ.

Then based on this personality analysis, provide brief advice on how managers and colleagues can work with this person effectively.

Transcript:
---
{transcript}
---

Return your answer in **valid JSON** format:
{{
  "openness": int (0-100),
  "conscientiousness": int (0-100),
  "extraversion": int (0-100),
  "agreeableness": int (0-100),
  "neuroticism": int (0-100),
  "iq": int,
  "eq": int,
  "advice_manager": str,
  "advice_colleagues": str,
  "reasoning": str
}}
"""
    )

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    return prompt | llm


def create_supabase_client(supabase_url: str, supabase_key: str):
    return create_client(supabase_url, supabase_key)


def fetch_transcript(supabase, unique_email: str):
    response = supabase.table("interviews").select("transcript").eq("unique_email", unique_email).execute()

    if not response.data:
        print(f"No transcript found for {unique_email}")
        return None

    return response.data[0]["transcript"]


def analyze_transcript(chain: RunnableSequence, transcript: str):
    result = chain.invoke({"transcript": transcript})
    try:
        return json.loads(result.content)
    except Exception as e:
        print("⚠️ Could not parse JSON. Output was:")
        print(result.content)
        return None


def main(unique_email: str):
    env = load_environment()
    supabase = create_supabase_client(env["supabase_url"], env["supabase_key"])
    transcript = fetch_transcript(supabase, unique_email)

    if not transcript:
        return

    chain = get_big_five_chain()
    result = analyze_transcript(chain, transcript)

    if result:
        return result

def insert_personality(unique_email: str, data: dict):
    env = load_environment()
    supabase = create_client(env["supabase_url"], env["supabase_key"])

    row = {
        "unique_email": unique_email,
        "openness": data["openness"],
        "conscientiousness": data["conscientiousness"],
        "extraversion": data["extraversion"],
        "agreeableness": data["agreeableness"],
        "neuroticism": data["neuroticism"],
        "iq": data["iq"],
        "eq": data["eq"],
        "advice_manager": data["advice_manager"],
        "advice_colleagues": data["advice_colleagues"],
        "reasoning": data["reasoning"],
    }

    response = supabase.table("personality").insert(row).execute()

    if response.data:
        print("✅ Personality data inserted.")
    else:
        print(f"❌ Failed to insert personality data. Response: {response}")


if __name__ == "__main__":
    email = "info@email.com"
    r = main(email)
    insert_personality(email, r)