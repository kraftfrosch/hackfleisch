from langchain_core.tools import tool
from pydantic import BaseModel, Field

from supabase_client import SUPABASE_CLIENT

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
def get_feedback_transcripts(employee_name: str, conversation_count: int = 1) -> str:
    """
    Get the last n conducted feedback interviews about an employee

    Args:
        employee_name (str): The name of the employee to get feedback transcripts for
        conversation_count (int): The number of conversations to return

    Returns:
        str: A string containing the transcripts of the last n conducted feedback interviews about the employee
    """
    response = SUPABASE_CLIENT.table("hack_conversations").select("transcript").order('start_time', desc=True).limit(conversation_count).execute()
    response = [convert_transcript_to_text(transcript) for transcript in response.data]
    return response

def get_relevant_competency_model(employee_name: str) -> str:
    """
    Get the relevant competeciy levels for an employee
    """

    relevant_competency_model = """
    Name: Ownership for collective achievement
    Description: Understand what needs to be done, take ownership of getting it over the finish line and do whatever it takes to get there while driving collective success
    Level 1: Consistently completes tasks to the expected time and quality, communicating any delays immediately.
    Level 2: Proficiently defines challenging and impactful goals and takes ownership for achieving them.
    Level 3: Shows great resilience in pushing through blockers, pushback, politics, or organizational boundaries to get things done.
    Level 4: Leads by example, consistently setting the standard for ownership, execution, and accountability across teams.
    """

    return relevant_competency_model


from typing import Literal

class Justification(BaseModel):
    type: Literal["positive", "negative", "actionable_advice"] = Field(description="The type of justification: positive for justifiactions that support the competency rating, negative for justifications that point out missing competencies for the next level, actionable_advice for justifications that provide advice on how to improve the competency.")
    justification: str = Field(description="The one sentence justification of the competency rating")
    quote: str = Field(description="A short quote from the transcript that supports the justification")

class CompetencyRating(BaseModel):
    competency_name: str = Field(description="The name of the competency")
    employee_level: int = Field(description="The level of the employee between 1 and 4")
    level_description: str = Field(description="The description of the level")
    justifications: list[Justification] = Field(description="The justifications for the competency rating")


@tool("gives_competency_rating", args_schema=CompetencyRating)
def gives_competency_rating(competency_name: str, employee_level: int, level_description: str, justifications: list[Justification]) -> str:
    """
    Give a employee a competency rating based on their competency model and transcripts of the feedback conversations.

    The rating should be created by comparing the feedback conversations to the competency descriptions and the employee's level in the competency model. The rating is paired with justifications which make clear why the rating was given and provide actionabel feedback for the employee.

    Returns:
        str: A string containing the competency rating
    """

    rating_json = {
        "competency_name": competency_name,
        "employee_level": employee_level,
        "level_description": level_description,
        "justifications": justifications
    }
    
    return json.dumps(rating_json)



