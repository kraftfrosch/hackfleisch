from langchain_core.tools import tool
from pydantic import BaseModel, Field
from supabase_client import SUPABASE_CLIENT
#from database_utils.save_transcriptions import get_agent_conversations


import ast
import json

def convert_transcript_to_text(transcript_obj):
    # Extract the string containing the list of messages
    transcript_str = transcript_obj['transcript']
    
    # Convert the string representation of a list of dicts into an actual Python list
    transcript_list = ast.literal_eval(transcript_str)
    
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
    Get the last n conducted feedback interviews about an employee

    Args:
        employee_name (str): The name of the employee to get feedback transcripts for

    Returns:
        list[str]: A list of strings containing the transcripts of the last n conducted feedback interviews about the employee
    """
    # agent_id = "Ye15B53h9unEaOVXYnKi"
    # df = get_agent_conversations(agent_id)

    response = SUPABASE_CLIENT.table("hack_conversations").select("transcript").eq("about_employee_name", employee_name).execute()
    if len(response.data) >= 1:
        response = [convert_transcript_to_text(transcript) for transcript in response.data]
        return response
    else:
        return "No feedback transcripts found for the employee"


from typing import Literal

class Justification(BaseModel):
    type: Literal["positive", "negative", "actionable_advice"] = Field(description="The type of justification: positive for justifiactions that support the competency rating, negative for justifications that point out missing competencies for the next level, actionable_advice for justifications that provide advice on how to improve the competency.")
    justification: str = Field(description="The one sentence justification of the competency rating")
    direct_quote: str = Field(description="A short direct quote from the transcript that supports the justification")

class CompetencyRating(BaseModel):
    competency_name: str = Field(description="The name of the competency")
    competency_description: str = Field(description="The description of the competency including all the level descriptions")
    employee_level: int = Field(description="The level of the employee between 1 and 4")
    justifications: list[Justification] = Field(description="The justifications for the competency rating")

class OverallRating(BaseModel):
    employee_name: str = Field(description="The name of the employee")
    competency_ratings: list[CompetencyRating] = Field(description="A list of all competency rating objects for the employee")


@tool("gives_competency_rating", args_schema=OverallRating)
def gives_competency_rating(employee_name: str, competency_ratings: list[CompetencyRating]) -> str:
    """
    Give an employee a rating for each competency based on the competency descriptions and transcripts of the feedback conversations.

    The rating should be created by comparing the feedback conversations to the competency descriptions and the employee's level and next level in the competency model. The rating is paired with justifications which make clear why the rating was given and provide actionabel feedback for the employee based on direct_quotes from the human during the conversation.

    Returns:
        str: A string containing the competency rating
    """
    try:
        for i, competency_rating in enumerate(competency_ratings):
            SUPABASE_CLIENT.table("employee").update({
                f"competency_name{i+1}": competency_rating.competency_name,
                f"competency_description{i+1}": competency_rating.competency_description,
                f"competency_currentlevel{i+1}": competency_rating.employee_level,
                f"justification{i+1}": [justification.model_dump() for justification in competency_rating.justifications]
            }).eq("Name", employee_name).execute()
    except Exception as e:
        return f"Error giving competency ratings: {e}"

    return "Competency ratings given successfully"



