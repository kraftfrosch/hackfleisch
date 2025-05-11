from elevenlabs import ElevenLabs
from typing import Dict, List, Tuple
from dataclasses import dataclass
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import os
import json
from transformers import pipeline

# Initialize Supabase client
db_web_link = "https://hkqvoplmxbycptpqjghe.supabase.co"
keyy = os.getenv('SUPABASE_KEY', "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhrcXZvcGxteGJ5Y3B0cHFqZ2hlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njg2ODA4MywiZXhwIjoyMDYyNDQ0MDgzfQ.wLT-6nThQhgXGREUEThA5Uzb6KcrU8ITwgGfTI_dd5A")
supabase: Client = create_client(db_web_link, keyy)

# Initialize zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_person(summary: str) -> str:
    """
    Use zero-shot classification to identify the person in the conversation.
    
    Args:
        summary (str): The conversation summary
        
    Returns:
        str: The identified person's name
    """
    candidate_labels = ["Vishwa", "Johannes", "Joshua", "Fabian", "Unknown"]
    
    # Get classification results
    result = classifier(summary, candidate_labels)
    
    # Get the label with highest score
    predicted_label = result['labels'][0]
    confidence = result['scores'][0]
    
    # If confidence is too low, return Unknown
    if confidence < 0.3:
        return "Unknown"
    
    return predicted_label

@dataclass
class TranscriptInfo:
    transcript: List[Dict[str, str]]
    summary: str
    first_message: str
    conversation_id: str
    start_time: datetime
    call_duration: int

def get_conversation_info(conversation_id: str) -> TranscriptInfo:
    """
    Extract transcript, summary, and first message from a conversation.
    
    Args:
        conversation_id (str): The ID of the conversation to analyze
        
    Returns:
        TranscriptInfo: Object containing transcript, summary, and first message
    """
    client = ElevenLabs(api_key="sk_9deb38b00186fbf1b004746fdb48ac30668ac58dd7b3e0e7")
    
    # Get conversation data
    conversation_data = client.conversational_ai.get_conversation(
        conversation_id=conversation_id
    )
    
    # Extract transcript
    transcript = []
    for message in conversation_data.transcript:
        transcript.append({
            'role': message.role,
            'message': message.message,
            'time_in_call_secs': message.time_in_call_secs
        })
    
    # Extract summary
    summary = conversation_data.analysis.transcript_summary
    
    # Extract first message
    first_message = conversation_data.conversation_initiation_client_data.conversation_config_override.agent.first_message
    
    # Extract metadata
    start_time = datetime.fromtimestamp(conversation_data.metadata.start_time_unix_secs)
    call_duration = conversation_data.metadata.call_duration_secs
    
    return TranscriptInfo(
        transcript=transcript,
        summary=summary,
        first_message=first_message,
        conversation_id=conversation_id,
        start_time=start_time,
        call_duration=call_duration
    )

def ensure_hack_conversations_table():
    """
    Ensure the hack_conversations table exists with all required columns.
    """
    try:
        # Create table with all required columns
        create_table_query = """
        CREATE TABLE IF NOT EXISTS hack_conversations (
            conversation_id text PRIMARY KEY,
            start_time timestamp with time zone,
            call_duration_secs integer,
            first_message text,
            summary text,
            transcript jsonb,
            message_count integer,
            status text,
            agent_name text,
            agent_id text,
            about_employee_name text
        );
        """
        supabase.rpc('exec_sql', {'query': create_table_query}).execute()
        print("Created hack_conversations table")
            
    except Exception as e:
        print(f"Error ensuring hack_conversations table: {str(e)}")

def store_conversation_in_supabase(conversation_data: dict):
    """
    Store conversation data in Supabase hack_conversations table.
    
    Args:
        conversation_data (dict): Dictionary containing conversation information
    """
    try:
        # Ensure table exists
        ensure_hack_conversations_table()
        
        # Convert datetime to ISO format string
        conversation_data['start_time'] = conversation_data['start_time'].isoformat()
        
        # Convert transcript list to JSON string
        conversation_data['transcript'] = json.dumps(conversation_data['transcript'])
        
        # Insert data into Supabase
        result = supabase.table('hack_conversations').insert(conversation_data).execute()
        
        if hasattr(result, 'error') and result.error:
            print(f"Error storing conversation {conversation_data['conversation_id']}: {result.error}")
        else:
            print(f"Successfully stored conversation {conversation_data['conversation_id']}")
            
    except Exception as e:
        print(f"Error storing conversation {conversation_data['conversation_id']}: {str(e)}")

def get_agent_conversations(agent_id: str) -> pd.DataFrame:
    """
    Fetch all successful conversations for a specific agent and store them in Supabase.
    
    Args:
        agent_id (str): The ID of the agent to fetch conversations for
        
    Returns:
        pd.DataFrame: DataFrame containing conversation information
    """
    client = ElevenLabs(api_key="sk_9deb38b00186fbf1b004746fdb48ac30668ac58dd7b3e0e7")
    
    # Get all successful conversations
    response = client.conversational_ai.get_conversations(
        call_successful="success"
    )
    
    # Filter conversations for specific agent and collect data
    conversation_data = []
    for conv in response.conversations:
        # Check if this conversation belongs to the specified agent
        if conv.agent_id == agent_id:
            try:
                info = get_conversation_info(conv.conversation_id)
                # Classify the person in the conversation
                person = classify_person(info.summary)
                
                data = {
                    'conversation_id': info.conversation_id,
                    'start_time': info.start_time,
                    'call_duration_secs': info.call_duration,
                    'first_message': info.first_message,
                    'summary': info.summary,
                    'transcript': info.transcript,
                    'message_count': conv.message_count,
                    'status': conv.status,
                    'agent_name': conv.agent_name,
                    'agent_id': agent_id,
                    'about_employee_name': person
                }
                conversation_data.append(data)
                # Store in Supabase
                store_conversation_in_supabase(data)
            except Exception as e:
                print(f"Error processing conversation {conv.conversation_id}: {str(e)}")
    
    # Create DataFrame for local reference
    df = pd.DataFrame(conversation_data)
    
    # Sort by start time
    df = df.sort_values('start_time', ascending=False)
    
    return df

# Example usage
if __name__ == "__main__":
    agent_id = "Ye15B53h9unEaOVXYnKi"
    df = get_agent_conversations(agent_id)
    
    # Display basic information
    print("\nConversation Overview:")
    print(f"Total conversations: {len(df)}")
    print("\nSample of conversations:")
    print(df[['conversation_id', 'start_time', 'call_duration_secs', 'summary', 'about_employee_name']].head())