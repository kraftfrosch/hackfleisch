from fastapi import FastAPI
from pydantic import BaseModel
from agent_module import run_agent
from typing import List, Dict
import uuid

app = FastAPI()

# In-memory storage for chat histories
chat_histories: Dict[str, List[dict]] = {}

class AgentRequest(BaseModel):
    input: str
    chat_id: str | None = None

@app.post("/run-agent")
async def invoke_agent(request: AgentRequest):
    try:
        # Generate a new chat_id if not provided
        chat_id = request.chat_id or str(uuid.uuid4())
        
        # Initialize chat history if it doesn't exist
        if chat_id not in chat_histories:
            chat_histories[chat_id] = []
            
        # Add user message to history
        chat_histories[chat_id].append({"role": "user", "content": request.input})
        
        # Run agent with chat history
        result = run_agent(request.input, chat_histories[chat_id])
        
        # Add assistant response to history
        chat_histories[chat_id].append({"role": "assistant", "content": result})
        
        return {
            "response": result,
            "chat_id": chat_id,
            "history": chat_histories[chat_id]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "LangChain HR Agent is running"}
