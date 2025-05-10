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

def get_skill_assessment_chain() -> RunnableSequence:
    prompt = PromptTemplate(
        input_variables=["transcript"],
        template="""
1. Skill Assessment of Employee X
Analyze the conversation to extract insights related to Employee X’s competencies and behaviors, based on the defined framework below.

Match any mentioned strengths or weaknesses to the appropriate skill category (e.g., Trustful Collaboration, Growth Mindset, System Design and Architecture, etc.).

For each relevant skill, assess which level (1–4) X likely demonstrates, using examples or quotes from the transcript if available.

If the skill or level is ambiguous, note the uncertainty.

In the following you can find all the skills and the respective level descriptions:

🛠️ Ownership for collective achievement
1: Completes tasks reliably; communicates delays; follows company protocols.

2: Sets challenging goals; reviews work to align with company standards.

3: Overcomes blockers and organizational boundaries; improves standards.

4: Sets execution culture; inspires teams toward shared, ambitious goals.

🤝 Trustful collaboration
1: Attends meetings, completes tasks, communicates reliably.

2: Helps structure team efforts; communicates effectively in meetings or wikis.

3: Improves collaboration; adapts communication to context and team needs.

4: Fosters psychological safety and shared accountability across teams.

⚡ Bias for action and positivity
1: Remains positive under pressure; moves forward independently.

2: Energizes others; offers simple, action-oriented solutions.

3: Boosts morale and action in tough environments; inspires through communication.

4: Builds a resilient, empowered culture aligned around action.

🌱 Growth Mindset
1: Responds to feedback respectfully; contributes when asked.

2: Proactively gives/asks for feedback; constructively raises improvement ideas.

3: Leads retrospectives; drives team-level improvement.

4: Champions feedback culture across teams; embeds learning in strategy.

🧩 System Design and Architecture
1: Understands design basics; contributes to technical discussions.

2: Designs scalable systems; identifies flaws and proposes improvements.

3: Anticipates scale/integration issues; leads architectural reviews.

4: Influences long-term architecture strategy; mentors others.

🧪 Code Quality and Craftsmanship
1: Follows code conventions; includes tests and documentation.

2: Writes clean, reusable code; contributes to code reviews.

3: Improves legacy codebases; leads refactoring efforts.

4: Defines quality standards; mentors and influences engineering practices.

⚙️ Technical Ownership and Reliability
1: Uses observability tools; escalates issues responsibly.

2: Owns services; sets up monitoring, logging, and alerting.

3: Leads incident reduction; drives operational excellence.

4: Builds reliable systems at scale; drives culture of reliability.

🤖 Model Development and Deployment
1: Trains/evaluates basic models using existing tools.

2: Deploys models; defines metrics; ensures stable performance.

3: Improves production models; automates model lifecycle.

4: Mentors and defines ML strategy at scale.

🧬 Data Understanding and Feature Engineering
1: Works with clean data; applies basic transformations.

2: Explores data; builds robust pipelines; handles imbalance.

3: Designs complex features; improves team data quality.

4: Shapes org-wide feature strategy; mentors on data practices.

🧠 Research Translation and Experimentation
1: Reads papers; tests small ideas from literature.

2: Applies research to practical use; designs hypothesis-based tests.

3: Leads translation projects; drives experimentation culture.

4: Shapes strategic AI adoption; builds experimentation frameworks.

🔍 Product Discovery and User Insight
1: Contributes to research or shares user insights.

2: Identifies and validates meaningful user problems.

3: Defines and drives domain-level product strategy.

4: Shapes company-wide product vision via user insight.

🗺️ Roadmapping and Prioritization
1: Assists in roadmap planning.

2: Owns roadmap; uses impact/effort to prioritize.

3: Manages cross-functional planning; adapts to outcomes.

4: Mentors others; sets standards across orgs.

📢 Stakeholder Communication and Alignment
1: Shares updates clearly; begins cross-functional interactions.

2: Coordinates with design/engineering to align work.

3: Anticipates conflicts and drives shared understanding.

4: Influences executives; aligns teams on product bets.

💡 Code-Until-It-Works Prototyping
1: Builds functional prototypes from templates or examples.

2: Combines APIs/scripts into working MVPs under time pressure.

3: Delivers stable MVPs fast with creativity.

4: Builds award-worthy hacks overnight from vague ideas.

☕ Sleep-Deprived Problem Solving
1: Stays productive during crunch through willpower alone.

2: Manages energy/snacks to stay sharp.

3: Mentors others on sustainable pressure management.

4: Keeps team focused and emotionally steady under pressure.

🎤 Demo Readiness and Pitch Hype
1: Communicates core ideas even if the demo is fragile.

2: Builds stable demo; brings humor/hype to presentation.

3: Polishes chaotic code into clean demo; pitches confidently.

4: Inspires and energizes audiences with vision and charisma.

Transcript:
---
{transcript}
---

Return your answer in **valid JSON** format (as an assessemt of the skill level of Employee X):
{{
  "Ownership for collective achievement": 1–4 or null,
  "Trustful collaboration": 1–4 or null,
  "Bias for action and positivity": 1–4 or null,
  "Growth Mindset": 1–4 or null,
  "System Design and Architecture": 1–4 or null,
  "Code Quality and Craftsmanship": 1–4 or null,
  "Technical Ownership and Reliability": 1–4 or null,
  "Model Development and Deployment": 1–4 or null,
  "Data Understanding and Feature Engineering": 1–4 or null,
  "Research Translation and Experimentation": 1–4 or null,
  "Product Discovery and User Insight": 1–4 or null,
  "Roadmapping and Prioritization": 1–4 or null,
  "Stakeholder Communication and Alignment": 1–4 or null,
  "Code-Until-It-Works Prototyping": 1–4 or null,
  "Sleep-Deprived Problem Solving": 1–4 or null,
  "Demo Readiness and Pitch Hype": 1–4 or null
}}
"""
    )





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


def fetch_transcript(supabase, unique_name: str):
    response = supabase.table("hack_conversation").select("transcript").eq("conversation_id", "qBqLblFEEQrWk7CGPqEC").execute()

    if not response.data:
        print(f"No transcript found for {unique_name}")
        return None
    print(response.data)
    return response.data[0]["transcript"]


def analyze_transcript(chain: RunnableSequence, transcript: str):
    result = chain.invoke({"transcript": transcript})
    try:
        return json.loads(result.content)
    except Exception as e:
        print("⚠️ Could not parse JSON. Output was:")
        print(result.content)
        return None


def main(unique_name: str):
    env = load_environment()
    supabase = create_supabase_client(env["supabase_url"], env["supabase_key"])
    transcript = fetch_transcript(supabase, unique_name)

    if not transcript:
        return

    chain = get_skill_assessment_chain()
    result = analyze_transcript(chain, transcript)

    if result:
        return result


def insert_skill_assessment(unique_name: str, data: dict):
    env = load_environment()
    supabase = create_client(env["supabase_url"], env["supabase_key"])

    row = {
    "unique_name": unique_name,
    "Ownership for collective achievement": data.get("Ownership for collective achievement"),
    "Trustful collaboration": data.get("Trustful collaboration"),
    "Bias for action and positivity": data.get("Bias for action and positivity"),
    "Growth Mindset": data.get("Growth Mindset"),
    "System Design and Architecture": data.get("System Design and Architecture"),
    "Code Quality and Craftsmanship": data.get("Code Quality and Craftsmanship"),
    "Technical Ownership and Reliability": data.get("Technical Ownership and Reliability"),
    "Model Development and Deployment": data.get("Model Development and Deployment"),
    "Data Understanding and Feature Engineering": data.get("Data Understanding and Feature Engineering"),
    "Research Translation and Experimentation": data.get("Research Translation and Experimentation"),
    "Product Discovery and User Insight": data.get("Product Discovery and User Insight"),
    "Roadmapping and Prioritization": data.get("Roadmapping and Prioritization"),
    "Stakeholder Communication and Alignment": data.get("Stakeholder Communication and Alignment"),
    "Code-Until-It-Works Prototyping": data.get("Code-Until-It-Works Prototyping"),
    "Sleep-Deprived Problem Solving": data.get("Sleep-Deprived Problem Solving"),
    "Demo Readiness and Pitch Hype": data.get("Demo Readiness and Pitch Hype"),
}


    response = supabase.table("skill_evaluations").insert(row).execute()

    if response.data:
        print("✅ Skill assessment data inserted.")
    else:
        print(f"❌ Failed to insert skill assessment data. Response: {response}")



def insert_personality(unique_name: str, data: dict):
    env = load_environment()
    supabase = create_client(env["supabase_url"], env["supabase_key"])

    row = {
        "unique_name": unique_name,
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
    name = "Fabian"
    r = main(name)
    insert_skill_assessment(name, r)
