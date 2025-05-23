from langchain_core.tools import tool
from pydantic import BaseModel, Field
from supabase_client import SUPABASE_CLIENT
from database_utils.save_transcriptions import get_agent_conversations


import json

def convert_transcript_to_text(transcript_obj):
    # Extract the string containing the list of messages
    transcript_str = transcript_obj['transcript']
    
    # Convert the string representation of a list of dicts into an actual Python list
    transcript_list = json.loads(transcript_str)
    
    # Initialize an empty list to collect the lines of conversation
    conversation = []

    # Process each message dictionary
    for entry in transcript_list:
        role = entry.get('role')
        message = entry.get('message')
        if message:
            speaker = 'Agent' if role == 'agent' else 'User'
            conversation.append(f"{speaker}: {message.strip()}")

    # Join all lines into a single text
    return "\n".join(conversation)


@tool("get_feedback_transcripts")
def get_feedback_transcripts(employee_name: str) -> list[str] | str:
    """
    Get all the conducted feedback interview transcripts about an employee

    Args:
        employee_name (str): The name of the employee to get feedback transcripts for

    Returns:
        list[str]: A list of strings containing the transcripts of conducted feedback interviews about the employee
    """
    agent_id = "Ye15B53h9unEaOVXYnKi"
    df = get_agent_conversations(agent_id)

    response = SUPABASE_CLIENT.table("hack_conversations").select("transcript").eq("about_employee_name", employee_name).execute()
    if len(response.data) >= 1:
        response = [convert_transcript_to_text(transcript) for transcript in response.data]
        return response
    else:
        return "No feedback transcripts found for the employee"


from typing import Literal

class Justification(BaseModel):
    type: Literal["positive", "negative", "actionable_advice"] = Field(description="The type of justification: positive for justifiactions that support the competency rating, negative for justifications that point out missing competencies for the next level, actionable_advice for justifications that provide advice on how to improve the competency.")
    justification: str = Field(description="The one sentence justification of the competency rating. Make is very consice and to the point.")
    direct_quote: str = Field(description="A short direct quote from the transcript that supports the justification. Keep it short and concise.")

class CompetencyRating(BaseModel):
    competency_name: str = Field(description="The name of the competency")
    competency_description: str = Field(description="The description of the competency including all the level descriptions")
    employee_level: int = Field(description="The level of the employee between 1 and 4")
    justifications: list[Justification] = Field(description="The justifications for the competency rating")

class Kudos(BaseModel):
    kudos_quote: str = Field(description="A direct quote from the transcript that is a kudos or appreciation for the employee")

class OverallRating(BaseModel):
    employee_name: str = Field(description="The name of the employee")
    competency_ratings: list[CompetencyRating] = Field(description="A list of all competency rating objects for the employee")
    kudos: list[Kudos] = Field(description="A list of all kudos for the employee")


@tool("gives_competency_rating", args_schema=OverallRating)
def gives_competency_rating(employee_name: str, competency_ratings: list[CompetencyRating], kudos: list[Kudos]) -> str:
    """
    Give an employee a rating for each of their four and only these four competencies based on the competency descriptions and what can be inferred about their level from the transcripts of the feedback conversations talking about them.

    The rating should be created by comparing the feedback conversations to the competency descriptions and the employee's level and next level in the competency model and see where the employee currently fits in best. The rating is paired with justifications which make clear why the rating was given or provide actionabel feedback for the employee.
    When possible include quotes from the transcripts (only from the human) to support the justification.

    Returns:
        str: A string containing the competency rating
    """
    try:
        for i, competency_rating in enumerate(competency_ratings):
            if i >= 5:
                break
            SUPABASE_CLIENT.table("employee").update({
                f"competency_name{i+1}": competency_rating.competency_name,
                f"competency_description{i+1}": competency_rating.competency_description,
                f"competency_currentlevel{i+1}": competency_rating.employee_level,
                f"justification{i+1}": [justification.model_dump() for justification in competency_rating.justifications]
            }).ilike("Name", employee_name).execute()

            SUPABASE_CLIENT.table("employee").update({
                f"kudos": [kudo.model_dump() for kudo in kudos]
            }).ilike("Name", employee_name).execute() 

    except Exception as e:
        return f"Error giving competency ratings: {e}"

    return "Competency ratings given successfully"



