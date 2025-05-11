import json
import requests
from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal
from supabase import create_client, Client
import os
import time
from tool_utils.slackbot import get_user_id_by_email, send_slack_message

# Initialize Supabase client
db_web_link = "https://hkqvoplmxbycptpqjghe.supabase.co"
keyy = os.getenv('SUPABASE_KEY', "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhrcXZvcGxteGJ5Y3B0cHFqZ2hlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njg2ODA4MywiZXhwIjoyMDYyNDQ0MDgzfQ.wLT-6nThQhgXGREUEThA5Uzb6KcrU8ITwgGfTI_dd5A")
supabase: Client = create_client(db_web_link, keyy)

def get_employee_from_db(name: str = None) -> str:
    """
    Get employee data from the database based on name.
    If name is None, returns all employees.
    
    Args:
        name: The name of the employee to search for. If None, returns all employees.
        
    Returns:
        A formatted string containing the employee(s) information
    """
    try:
        # Query the employee table
        if name:
            response = supabase.table("employee").select("*").ilike('Name', f'%{name}%').execute()
        else:
            response = supabase.table("employee").select("*").execute()
        
        if response.data:
            if name:
                employee = response.data[0]  # Get the first matching result
                result = f"""
                        Name: {employee['Name']}
                        Role: {employee.get('role', 'N/A')}
                        Bio: {employee.get('bio', 'N/A')}
                        Phone: {employee.get('phone', 'N/A')}
                        Project Responsibilities: {employee.get('project_responsibilities', 'N/A')}
                        """
                
                # Add competencies
                for i in range(1, 5):
                    comp_name = employee.get(f'competency_name{i}')
                    if comp_name:
                        result += f"""
                        Competency {i}:
                        - Name: {comp_name}
                        - Description: {employee.get(f'compentency_description{i}', 'N/A')}
                        - Current Level: {employee.get(f'competency_currentlevel{i}', 'N/A')}
                        - Proposed Level: {employee.get(f'competency_proposed_level{i}', 'N/A')}
                        - Justification: {employee.get(f'justification{i}', 'N/A')}
                        """
                
                return result
            else:
                # Format all employees
                result = "Employee Directory:\n" + "=" * 80 + "\n"
                for employee in response.data:
                    result += f"""
                                Name: {employee['Name']}
                                Role: {employee.get('role', 'N/A')}
                                Bio: {employee.get('bio', 'N/A')}
                                Phone: {employee.get('phone', 'N/A')}
                                Project Responsibilities: {employee.get('project_responsibilities', 'N/A')}
                                """
                    
                    # Add competencies
                    for i in range(1, 5):
                        comp_name = employee.get(f'competency_name{i}')
                        if comp_name:
                            result += f"""
                                Competency {i}:
                                - Name: {comp_name}
                                - Description: {employee.get(f'compentency_description{i}', 'N/A')}
                                - Current Level: {employee.get(f'competency_currentlevel{i}', 'N/A')}
                                - Proposed Level: {employee.get(f'competency_proposed_level{i}', 'N/A')}
                                - Justification: {employee.get(f'justification{i}', 'N/A')}
                                """
                    
                    result += f"{'-' * 80}\n"
                
                result += f"\nTotal employees found: {len(response.data)}"
                return result
        else:
            return f"No employees found" if name is None else f"No employee found with name containing '{name}'"
            
    except Exception as e:
        return f"Error retrieving employee data: {str(e)}"

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
    employee_info: str = Field(description="All information about the employee, including team, competencies etc")
    questions: str = Field(description="An elaborate list of questions, tailored towards the person. Most important part, therefore needs to be very detailed.")
    send_feedback_to: list[str] = Field(description='The name of the employee this feedback is being sent to. String for each employee should contain their name, team, project etc. Most likely a colleagues of the employee who the feedback is on. Explicitly ask for the names of colleagues you would collect feedback from.')
    details_of_send_feedback_to: list[str] = Field(description='The list of information about the employees this feedback is to be sent to. String for each employee should contain their name, team, project etc. Most likely a colleagues of the employee who the feedback is on. Explicitly ask for the names of colleagues you would collect feedback from.')
    phone_number:list[str] = Field(description="List of phone numbers of people to be called. Default values are the numbers of their teammates. Get the phone numbers from the employee database, by querying the employee the feedback is being sent to.")
    

@tool("create_questionnaire", args_schema=Questionnaire)
def conduct_feedback(questionnaire_id: int, employee_name: str, employee_info:str, questions: str, send_feedback_to: str, details_of_send_feedback_to: str, phone_number: list) -> str:
    """
    Creates a feedback questionnaire based of individualized questions from the context of an employee and call coworkers to collect it.

    Questions should be written like from an HR expert specializing in performance evaluations. 
    The task is to create personalized feedback questionnaires after a project based on the employee's project involvement, current and targeted competencies, and growth goals which their project team can fill out. 
    The questions should be specific to the project and the responsibilities and role the employee had in this project. Use project context on what they contributed and 
    people collaborated to pick up on interactions and deliverables within the questions (e.g. a collaborative workshop, important milestone presentation, quality of work of a deliverable etc.). 
    The questions should try to specifically evaluate the development areas i.e. the employee growth goals and the descriptions of their targeted competency progression. 
    Your goal is to generate questions that teammates can answer to help the employee grow effectively. The questions should be clear, easy to understand and not too long. 
    Questions can be either of type open-ended, rating (from 1 to 6) with a label or multiple-choice.
    
    Returns:
        Were the feedback calls successful. If yes, theyll be collected and processed shortly.
    """

    # Creates a string with all the questions with newlines between them
    # questions_string = "\n".join([question.question for question in questions])

    # Creates a prompt for a call agent to conduct a voice call to ask the questions and follow up where needed.

    if len(phone_number) == 0:
        phone_number = ["+4915510483448"]

    # phone_number = ["+4915510483448"]
    # send_feedback_to = ['Default User']
    # details_of_send_feedback_to = ['Just the default user']

    successes = []
    for name, info, p in zip(send_feedback_to, details_of_send_feedback_to, phone_number):

        print(f"Calling {p}, name: {name}, info: {info}")

        call_prompt = f"""
        You are Christina, an HR professional conducting a feedback call with the following person named {name}. There is their info:\n

        {info}
        
        You are asking question about their coworker {employee_name}. The goal of the call is to gather honest, constructive feedback to support their professional development and performance growth. Keep the call focused, respectful, and efficient—do not veer off-topic or engage in small talk. Your tone should be neutral and professional at all times.
        Here is the information about {employee_name}:\n

        {employee_info}
        
        Ask each of the following questions clearly and wait for a complete response before proceeding. Where appropriate, ask brief follow-up questions to clarify vague statements, request specific examples, or guide the feedback toward development-oriented insights. Follow-up questions should be used to improve the quality of responses by making them more actionable and relevant to performance and growth. Use best practices for effective feedback collection—focus on behavior, outcomes, and potential improvements.

        Here are the questions to ask:

        {questions}

        End the call by thanking the coworker for their time and thoughtful input. Let them know their responses will be kept confidential and used solely to support {employee_name}’s development.
        """

        response = requests.post(
            "https://steady-handy-sculpin.ngrok-free.app/outbound-call",
            headers={"Content-Type": "application/json"},
            json={
                "prompt": call_prompt,
                "first_message": f"Hey {name}, my name is Christina, I wanted to quickly chat with you about your project with {employee_name} and potential feedback you might have.",
                "number": p
            }
        )

        time.sleep(1)

        print("Full API Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Content: {response.text}")
        print("=" * 80)

        successes.append(response)
        break

    return f"Calls successful: {str(successes)}"


# class FeedbackCall(BaseModel):
#     prompt: str = Field(description="The prompt for the call agent")
#     employee_name: str = Field(description="The name of the employee the feedback survey is about")
#     call_recipient: str = Field(description="The name of the coworker to call")


# @tool("call_coworker", args_schema=FeedbackCall)
# def call_coworker(prompt: str, employee_name: str,call_recipient: str) -> str:
#     """
#     Calls a coworker and asks them the questions.
#     """
    
#     response = requests.post(
#         "https://steady-handy-sculpin.ngrok-free.app/outbound-call",
#         headers={"Content-Type": "application/json"},
#         json={
#             "prompt": prompt,
#             "first_message": f"Hey {call_recipient}, my name is Chris, I wanted to quickly chat with you about your project with {employee_name} and potential feedback you might have.",
#             "number": "+4915753227687"
#         }
#     )

#     return response.json()


# @tool("send_feedback_questionnaire_message")
# def send_feedback_questionnaire_message(receipients: list[str], questionnaire_link: str) -> list[str]:
#     """
#     Sends a reminder to the list of receipients to fill out the feedback questionnaire.

#     Args:
#         receipients: The list of receipient emails to send the message to
#         questionnaire_link: The link to the feedback questionnaire

#     Returns:
#         A list of the receipients that were sent the message
#     """
    
#     for user in receipients:
#         if user_id := get_user_id_by_email(user):
#             message = f"Hi there! Please take some time to jump on a call and give some feedback on {user}. Here is the link: {questionnaire_link}"
#             send_slack_message(user_id, message)
#         else:
#             receipients.remove(user)
#             print(f"User {user} not found.")

#     print(receipients)


@tool("get_employee_context")
def get_employee_context(employee_name: str) -> str:
    """
    Gets the relevant context for employee feedback. This includes the employee's data, project involvment, phone number, competencies etc.

    Args:
        employee_name: The name of the employee to get the context for.

    Returns:
        A string containing the employee's project involvement, current and targeted competencies, and growth goals.
    """
    # Try to get employee data from database first
    db_data = get_employee_from_db(employee_name)
    
    # For now, return Fabian's context as fallback
    if "No employee found" in db_data or "Error" in db_data:
        Fabian_context = "Here is the context of the employee Fabian:\n\nName: Fabian\nTitle: Software Engineer\nCurrent and targeted competencies descriptions: \nCompetency: Ownership for collective achievement\nType: Core\nCurrent level description: Proficiently defines challenging and impactful goals and takes ownership for achieving them.\nTarget level description: Shows exceptional resilience in pushing through blockers, pushback, politics, or organizational boundaries to get things done.\n\nCompetency: Bias for action and positivity\nType: Core\nCurrent level description: Stays positive, open and active in the face of failure, challenges or setbacks.\nTarget level description: Energizes others in tough situations with recognition, shout-outs, inspiration about project goals and a strong positive attitude.\n\nCompetency: Code-Until-It-Works Prototyping\nType: Functional\nCurrent level description: Builds fast, functional prototypes that demonstrate core ideas and test technical feasibility under time pressure.\nTarget level description: Combines rapid prototyping with smart abstraction—delivers robust, demo-ready solutions that can evolve beyond the hackathon without a total rewrite.\n\nCompetency: Sleep Management & Latenight coding\nType: Functional\nCurrent level description: Pulls all-nighters with minimal caffeine crashes and keeps their local server alive through sheer willpower.\nTarget level description: Helps teams stay focused and sane, even at 4AM, while delivering something unforgettable.\n\nCompetency: Demo Readiness and Pitch Execution\nType: Functional\nCurrent level description: Pitches ideas with clarity and conviction. Don't loses the threat or seems to be nervous.\nTarget level description: Executes pitches with energy, charisma, and a clear focus on the audience's needs.\n\nDevelopment goals: \nI want to advance in my skills to pitch and sell my ideas in front of a critical audience. Especially beeing execelnt in communicating technical topics to non-technical people.\nGet a better understanding and inital first hand experience in bringing a AI agent in production.\n\n\nProject Name: CDTM Hackathon Weekend\nProject Description: \nA 2 day hackathon in munich to build AI agents to automate real world processes end-to-end. The team works 36 hours to come up with an idea, business case and to build a prototype until late at night. All will lead to a final pitch to present the idea, technology and the business case to a jury of experts.\n\nWe started with a few hour brainstroming session on friday to narrow down an idea with a potential winning edge. On Staturday we drew down the system arcitecture and tried to walk through the user jounrney again to the devide the parts of the development. On Satureday evening Fabian and Johannes created a storyline for the video production and refined the business case. On Saturday the whole team presented the idea, technology and the business case to a jury of experts with Fabian taking a lead on the Q&A.\n\nProject Goal: Build a working version of an AI agent faciliating real-time feedback and culture mining in a company.\nEmployee's Project role: Hacker - Tech/Business\nEmployee's responsibilities within the project: Setting up supabase and integrating it with all components of the app. Facilitating the team work and mini-sprints. Owning the video prodcution for the final submission and pitch\n\nPlease generate a feedback questionnaire based on that information that teammates can fill out according to the instructions."
        return Fabian_context
    
    return db_data

@tool("get_basic_employee_info")
def get_basic_employees_list() -> str:
    """
    Gets basic information about all employees including their name, role, bio, project, and phone number.
    
    Returns:
        A formatted string containing the basic information for all employees
    """
    try:
        response = supabase.table("employee").select("Name, role, bio, project, phone").execute()
        
        if response.data:
            result = "Employee Directory:\n" + "=" * 80 + "\n"
            for employee in response.data:
                result += f"""
                        Name: {employee['Name']}
                        Role: {employee.get('role', 'N/A')}
                        Bio: {employee.get('bio', 'N/A')}
                        Project: {employee.get('project', 'N/A')}
                        Phone: {employee.get('phone', 'N/A')}
                        {'-' * 80}
                        """
            result += f"\nTotal employees found: {len(response.data)}"
            return result
        else:
            return "No employees found in the database"
            
    except Exception as e:
        return f"Error retrieving employee data: {str(e)}"

