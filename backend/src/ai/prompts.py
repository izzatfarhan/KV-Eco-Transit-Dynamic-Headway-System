from langchain_core.prompts import PromptTemplate

# ---------------------------------------------------------
# TEXT-TO-SQL PROMPTS
# ---------------------------------------------------------
# Schema Safety: We explicitly instruct the LLM to only run SELECT statements.
TEXT_TO_SQL_PROMPT_TEMPLATE = """You are a PostgreSQL expert analyzing transit data for the Klang Valley Eco-Transit Optimizer.
Given an input question, create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer.

CRITICAL SECURITY RULE: You must NEVER generate queries that modify the database (e.g., DROP, DELETE, UPDATE, INSERT, ALTER).
Only generate SELECT statements.

You have access to the following tables and their schema:
{table_info}

Question: {input}
"""

text_to_sql_prompt = PromptTemplate.from_template(TEXT_TO_SQL_PROMPT_TEMPLATE)

# ---------------------------------------------------------
# CRISIS BROADCAST PROMPTS
# ---------------------------------------------------------
CRISIS_BROADCAST_PROMPT_TEMPLATE = """You are the automated communications agent for the Klang Valley rail transit network.
An infrastructure anomaly has been detected: {anomaly_description}.
Location: {station_name}

Your task is to author a localized crisis broadcast alert.
Generate the response in a JSON format containing three fields:
1. "tts_english": A short, calm announcement suitable for Text-to-Speech playback at the station (English).
2. "tts_malay": The equivalent Text-to-Speech announcement in Bahasa Malaysia.
3. "social_media": A concise, informative push notification/social media post (bilingual or English) including hashtags.

Do not include any other conversational text outside the JSON.
"""

crisis_broadcast_prompt = PromptTemplate.from_template(CRISIS_BROADCAST_PROMPT_TEMPLATE)
