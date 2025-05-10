import json
from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal

from slackbot import get_user_id_by_email, send_slack_message

class Option(BaseModel):
    rating: int = Field(description="The rating of the option from 1 to 6. Is None for Questions of type choice.")
    label: str = Field(description="The label of the option.")

class Question(BaseModel):
    type: Literal["open", "rating", "choice"] = Field(description="The type of the question. Open is an open-ended question, rating is a question with a rating scale from 1 to 6 and choice is a question with 2-4 multiple choice options.")
    question: str = Field(description="The question to be asked")
    options: list[Option] = Field(description="The list of Options to be given for the question in case it is rating or choice. None if type is open")

class Questionnaire(BaseModel):
    questionnaire_id: int = Field(description="The id of the questionnaire")
    employee_name: str = Field(description="The name of the employee the feedback survey is about")
    questions: list[Question] = Field(description="The list of questions to be asked")
    

@tool("create_questionnaire", args_schema=Questionnaire)
def create_questionnaire(questionnaire_id: int, employee_name: str,questions: list[Question]) -> str:
    """
    Creates a feedback questionnaire based of individualized questions from the context of an employee.

    Questions should be written like from an HR expert specializing in performance evaluations. The task is to create personalized feedback questionnaires after a project based on the employee's project involvement, current and targeted competencies, and growth goals which their project team can fill out. The questions should be specific to the project and the responsibilities and role the employee had in this project. Use project context on what they contributed and where people collaborated to pick up on interactions and deliverables within the questions (e.g. a collaborative workshop, important milestone presentation, quality of work of a deliverable etc.). The questions should try to specifically evaluate the development areas i.e. the employee growth goals and the descriptions of their targeted competency progression. Your goal is to generate questions that teammates can answer to help the employee grow effectively. The questions should be clear, easy to understand and not too long. Questions can be either of type open-ended, rating (from 1 to 6) with a label or multiple-choice.

    Some examples of good questions are:
    "To what extent did Samuel demonstrate his ability to push through blockers or organizational boundaries to deliver on his responsibilities like securing the initial meeting with SAP?"
    "What has been your overall impression on the impact of John for getting the first version of the website up and running on time?"
    "What areas of improvement and competence did you notice during the external Workshop with BOSCH for Lena in respect of making everyone feel heard and valued?"
    "Do you recall any specific situations where Johannes showed exceptional strong negotiation skills and why it impressed you?"
    "How do you feel Lisa handled the conflict around the project escalation from Jürgen (BMW) as a project lead?"

    Returns:
        A link to the questionnaire to be filled out
    """

    # Creates a string with all the questions with newlines between them
    questions_string = "\n".join([question.question for question in questions])

    # Creates a prompt for a call agent to conduct a video call to ask the questions and follow up where needed.
    prompt = f"""
    You are an AI assistant conducting a feedback call with a coworker of {employee_name}. The goal of the call is to gather honest, constructive feedback to support their professional development and performance growth. Keep the call focused, respectful, and efficient—do not veer off-topic or engage in small talk. Your tone should be neutral and professional at all times.

    Ask each of the following questions clearly and wait for a complete response before proceeding. Where appropriate, ask brief follow-up questions to clarify vague statements, request specific examples, or guide the feedback toward development-oriented insights. Follow-up questions should be used to improve the quality of responses by making them more actionable and relevant to performance and growth. Use best practices for effective feedback collection—focus on behavior, outcomes, and potential improvements.

    Here are the questions to ask:

    {questions_string}

    End the call by thanking the coworker for their time and thoughtful input. Let them know their responses will be kept confidential and used solely to support {employee_name}’s development.
    """

    with open("../../data/survey_prompt.json", "w") as f:
        f.write(json.dumps({"call_id": questionnaire_id, "call_prompt": prompt}))
    # subprocess.run(["bash", "...", "-.", "survey_prompt.json"])


    print(questionnaire_id, questions)
    return "https://www.google.com"

@tool("send_feedback_questionnaire_message")
def send_feedback_questionnaire_message(receipients: list[str], questionnaire_link: str) -> list[str]:
    """
    Sends a reminder to the list of receipients to fill out the feedback questionnaire.

    Args:
        receipients: The list of receipient emails to send the message to
        questionnaire_link: The link to the feedback questionnaire

    Returns:
        A list of the receipients that were sent the message
    """
    
    for user in receipients:
        if user_id := get_user_id_by_email(user):
            message = f"Hi there! Please take some time to jump on a call and give some feedback on {user}. Here is the link: {questionnaire_link}"
            send_slack_message(user_id, message)
        else:
            receipients.remove(user)
            print(f"User {user} not found.")

    print(receipients)


@tool("get_employee_context")
def get_employee_context(employee_name: str) -> str:
    """
    Gets the relevant context for employee feedback. This includes the employee's project involvement, current and targeted competencies, and growth goals.

    Args:
        employee_name: The name of the employee to get the context for

    Returns:
        A string containing the employee's project involvement, current and targeted competencies, and growth goals.
    """
    
    Fabian_context = "Here is the context of the employee Fabian:\n\nName: Fabian\nTitle: Software Engineer\nCurrent and targeted competencies descriptions: \nCompetency: Ownership for collective achievement\nType: Core\nCurrent level description: Proficiently defines challenging and impactful goals and takes ownership for achieving them.\nTarget level description: Shows exceptional resilience in pushing through blockers, pushback, politics, or organizational boundaries to get things done.\n\nCompetency: Bias for action and positivity\nType: Core\nCurrent level description: Stays positive, open and active in the face of failure, challenges or setbacks.\nTarget level description: Energizes others in tough situations with recognition, shout-outs, inspiration about project goals and a strong positive attitude.\n\nCompetency: Code-Until-It-Works Prototyping\nType: Functional\nCurrent level description: Builds fast, functional prototypes that demonstrate core ideas and test technical feasibility under time pressure.\nTarget level description: Combines rapid prototyping with smart abstraction—delivers robust, demo-ready solutions that can evolve beyond the hackathon without a total rewrite.\n\nCompetency: Sleep Management & Latenight coding\nType: Functional\nCurrent level description: Pulls all-nighters with minimal caffeine crashes and keeps their local server alive through sheer willpower.\nTarget level description: Helps teams stay focused and sane, even at 4AM, while delivering something unforgettable.\n\nCompetency: Demo Readiness and Pitch Execution\nType: Functional\nCurrent level description: Pitches ideas with clarity and conviction. Don't loses the threat or seems to be nervous.\nTarget level description: Executes pitches with energy, charisma, and a clear focus on the audience's needs.\n\nDevelopment goals: \nI want to advance in my skills to pitch and sell my ideas in front of a critical audience. Especially beeing execelnt in communicating technical topics to non-technical people.\nGet a better understanding and inital first hand experience in bringing a AI agent in production.\n\n\nProject Name: CDTM Hackathon Weekend\nProject Description: \nA 2 day hackathon in munich to build AI agents to automate real world processes end-to-end. The team works 36 hours to come up with an idea, business case and to build a prototype until late at night. All will lead to a final pitch to present the idea, technology and the business case to a jury of experts.\n\nWe started with a few hour brainstroming session on friday to narrow down an idea with a potential winning edge. On Staturday we drew down the system arcitecture and tried to walk through the user jounrney again to the devide the parts of the development. On Satureday evening Fabian and Johannes created a storyline for the video production and refined the business case. On Saturday the whole team presented the idea, technology and the business case to a jury of experts with Fabian taking a lead on the Q&A.\n\nProject Goal: Build a working version of an AI agent faciliating real-time feedback and culture mining in a company.\nEmployee's Project role: Hacker - Tech/Business\nEmployee's responsibilities within the project: Setting up supabase and integrating it with all components of the app. Facilitating the team work and mini-sprints. Owning the video prodcution for the final submission and pitch\n\nPlease generate a feedback questionnaire based on that information that teammates can fill out according to the instructions."
    return Fabian_context