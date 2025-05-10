from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from questionnair_tool import conduct_feedback, get_employee_context
from memory import (
    WRAP_FUNCTION_MAPPING,
    MemoryItem,
    Role,
    MEMORY_DELL_DIR,
    save_memory_general,
    load_memory_general,
)
# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0
)
from langchain import hub


# Define the system message
system_message = """You are an expert HR assistant specialized in feedback management. Your main job is to assist the user with feedback management.
You have tools to access the employee informations, create feedback and send feedback calls to people.
Use create questionaire to make a questionaire for an employee and send the feedback collection over via call. To get employee data, use get_employee_context."""

# Create the prompt template
# prompt = ChatPromptTemplate.from_messages([
#     ("system", system_message),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("human", "{input}"),
#     MessagesPlaceholder(variable_name="agent_scratchpad"),
# ])


def save_message_history_for(chat_id: str, messages: list[MemoryItem]) -> None:
        save_memory_general(chat_id, messages, MEMORY_DELL_DIR)

def run_agent(user_input: str, chat_id: int) -> str:
    memory_items = load_memory_general(chat_id, MEMORY_DELL_DIR)
    messages = [SystemMessage(system_message)] + [
            WRAP_FUNCTION_MAPPING[item.role](content=item.content)
            for item in memory_items
        ]
    
    # Define the tools
    tools = [conduct_feedback, get_employee_context]
    prompt = hub.pull("hwchase17/openai-tools-agent")

    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    response = agent_executor.invoke({"input": user_input, "chat_history": messages})
    text_resp = response["output"]

    ## Saving memory
    memory_items.append(MemoryItem(role=Role.USER, content=user_input))
    memory_items.append(MemoryItem(role=Role.ASSISTANT, content=text_resp))
    save_message_history_for(chat_id, memory_items)

    return text_resp


if __name__ == '__main__':
    run_agent('What info do you need?', 1)