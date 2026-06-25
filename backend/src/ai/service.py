import os
import logging
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_openrouter import ChatOpenRouter
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END

from src.ai.prompts import text_to_sql_prompt, crisis_broadcast_prompt

logger = logging.getLogger(__name__)

os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "dummy_key")

llm = ChatOpenRouter(
    model="openai/gpt-oss-120b:free",
    temperature=0,
)

# ---------------------------------------------------------
# TEXT-TO-SQL LANGGRAPH AGENT
# ---------------------------------------------------------
class AgentState(TypedDict):
    input: str
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sql_query: str
    db_result: str
    final_answer: str

def generate_sql(state: AgentState):
    """Generates the SQL query based on user input and schema."""
    logger.info("Generating SQL...")
    schema_info = "stations(station_id, name, line_name, current_crowd_density)\ntrains(train_id, current_station_id, status, headway_buffer_seconds)"
    
    chain = text_to_sql_prompt | llm
    response = chain.invoke({"table_info": schema_info, "input": state["input"]})
    
    sql_query = response.content.strip().replace("```sql", "").replace("```", "")
    return {"sql_query": sql_query}

def execute_sql(state: AgentState):
    """Executes the generated SQL query securely (Read-Only)."""
    logger.info(f"Executing SQL: {state['sql_query']}")
    if any(keyword in state['sql_query'].upper() for keyword in ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]):
        return {"db_result": "ERROR: Modifying queries are not allowed."}
    
    result = "Mocked DB Result" # Using mocked DB result
    return {"db_result": str(result)}

def generate_answer(state: AgentState):
    """Generates final human-readable answer from DB results."""
    logger.info("Generating final answer...")
    prompt = f"Question: {state['input']}\nSQL Query: {state['sql_query']}\nDB Result: {state['db_result']}\nProvide a clear answer."
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_answer": response.content}

# Build the Text-to-SQL Graph
workflow = StateGraph(AgentState)
workflow.add_node("generate_sql", generate_sql)
workflow.add_node("execute_sql", execute_sql)
workflow.add_node("generate_answer", generate_answer)

workflow.set_entry_point("generate_sql")
workflow.add_edge("generate_sql", "execute_sql")
workflow.add_edge("execute_sql", "generate_answer")
workflow.add_edge("generate_answer", END)

text_to_sql_app = workflow.compile()


# ---------------------------------------------------------
# CRISIS BROADCAST GENERATOR
# ---------------------------------------------------------
async def generate_crisis_broadcast(anomaly_description: str, station_name: str) -> str:
    """
    Triggers the LLM agent to instantly author localized English/Malay alert scripts.
    """
    logger.info(f"Generating Crisis Broadcast for {station_name}: {anomaly_description}")
    chain = crisis_broadcast_prompt | llm
    
    response = await chain.ainvoke({
        "anomaly_description": anomaly_description,
        "station_name": station_name
    })
    
    return response.content
