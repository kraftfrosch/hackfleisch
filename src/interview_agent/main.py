from fastapi import FastAPI
from pydantic import BaseModel
from agent_module import run_agent
from typing import List, Dict
from memory import (
    WRAP_FUNCTION_MAPPING,
    MemoryItem,
    Role,
    MEMORY_DELL_DIR,
    save_memory_general,
    load_memory_general,
)
from fastapi.middleware.cors import CORSMiddleware
import uuid
from database_utils.save_transcriptions import get_agent_conversations

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for chat histories

class AgentRequest(BaseModel):
    input: str
    chat_id: str | None = None

@app.post("/run-agent")
async def invoke_agent(request: AgentRequest):
    try:
        # Generate a new chat_id if not provided
        chat_id = request.chat_id or str(uuid.uuid4())

        #Load chat history
        history = load_memory_general(chat_id, MEMORY_DELL_DIR)

        # Run agent with chat history
        result = run_agent(request.input, chat_id)
        
        return {
            "response": result,
            "chat_id": chat_id,
            "history": history,
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "LangChain HR Agent is running"}

@app.get("/fetch_information")
async def fetch_information():
    '''
    Fetch all the conversations from Eleven labs to Supabase
    '''
    agent_id = "Ye15B53h9unEaOVXYnKi"
    df = get_agent_conversations(agent_id)
    return df.to_dict(orient="records")
