#from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from PROMPTS.PROMPT_SYSTEM_questionnair import questionnaire_system_prompt
from PROMPTS.PROMPT_INSTRUCT_questionnair import questionnaire_instruct_prompt_template, questionnaire_instruct_input_variables

from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(model="gpt-4o").with_structured_output(method="json_mode")


system_prompt = SystemMessage(questionnaire_system_prompt)
human_prompt = HumanMessagePromptTemplate.from_template(questionnaire_instruct_prompt_template, input_variables=questionnaire_instruct_input_variables)
prompt_template = ChatPromptTemplate.from_messages(
    [system_prompt, human_prompt]
)

current_and_targeted_competencies_Fabian = """
Competency: Ownership for collective achievement
Type: Core
Current level description: Proficiently defines challenging and impactful goals and takes ownership for achieving them.
Target level description: Shows exceptional resilience in pushing through blockers, pushback, politics, or organizational boundaries to get things done.

Competency: Bias for action and positivity
Type: Core
Current level description: Stays positive, open and active in the face of failure, challenges or setbacks.
Target level description: Energizes others in tough situations with recognition, shout-outs, inspiration about project goals and a strong positive attitude.

Competency: Code-Until-It-Works Prototyping
Type: Functional
Current level description: Builds fast, functional prototypes that demonstrate core ideas and test technical feasibility under time pressure.
Target level description: Combines rapid prototyping with smart abstraction—delivers robust, demo-ready solutions that can evolve beyond the hackathon without a total rewrite.

Competency: Sleep Management & Latenight coding
Type: Functional
Current level description: Pulls all-nighters with minimal caffeine crashes and keeps their local server alive through sheer willpower.
Target level description: Helps teams stay focused and sane, even at 4AM, while delivering something unforgettable.

Competency: Demo Readiness and Pitch Execution
Type: Functional
Current level description: Pitches ideas with clarity and conviction. Don't loses the threat or seems to be nervous.
Target level description: Executes pitches with energy, charisma, and a clear focus on the audience's needs.
"""

development_goals_Fabian = """
I want to advance in my skills to pitch and sell my ideas in front of a critical audience. Especially beeing execelnt in communicating technical topics to non-technical people.
Get a better understanding and inital first hand experience in bringing a AI agent in production.
"""

project_description_CDTM_Hackathon = """
A 2 day hackathon in munich to build AI agents to automate real world processes end-to-end. The team works 36 hours to come up with an idea, business case and to build a prototype until late at night. All will lead to a final pitch to present the idea, technology and the business case to a jury of experts.

We started with a few hour brainstroming session on friday to narrow down an idea with a potential winning edge. On Staturday we drew down the system arcitecture and tried to walk through the user jounrney again to the devide the parts of the development. On Satureday evening Fabian and Johannes created a storyline for the video production and refined the business case. On Saturday the whole team presented the idea, technology and the business case to a jury of experts with Fabian taking a lead on the Q&A.
"""

messages = prompt_template.format_messages(
    full_name="Fabian",
    title="Software Engineer",
    current_and_targeted_competencies=current_and_targeted_competencies_Fabian,
    development_goals=development_goals_Fabian,
    project_name="CDTM Hackathon Weekend",
    project_description=project_description_CDTM_Hackathon,
    project_goal="Build a working version of an AI agent faciliating real-time feedback and culture mining in a company.",
    project_role="Hacker - Tech/Business",
    project_responsibilities="Setting up supabase and integrating it with all components of the app. Facilitating the team work and mini-sprints. Owning the video prodcution for the final submission and pitch")
message = model.invoke(messages)

print(message)