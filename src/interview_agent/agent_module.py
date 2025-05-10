from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from questionnair_tool import create_questionnaire, get_employee_context, call_coworker

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0
)

# Define the system message
system_message = """You are an expert HR assistant specialized in creating personalized feedback questionnaires.
Your task is to help create detailed feedback questionnaires for employees based on their project involvement, competencies, and growth goals.
Use the provided tools to gather employee context and create appropriate questionnaires.
Always ensure the questions are specific, relevant, and aligned with the employee's development goals."""

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_message),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Define the tools
tools = [create_questionnaire, get_employee_context, call_coworker]

# Create the agent
agent = create_openai_functions_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

def run_agent(user_input: str, chat_history: list[dict]) -> str:
    return agent_executor.invoke({"input": user_input, "chat_history": chat_history})