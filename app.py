from langchain_ollama import OllamaLLM
import json
from langchain.prompts import PromptTemplate
from prompt import PROMPT_TEMPLATE
from utils import extract_sql_query,get_schema
import duckdb
import pandas as pd

with open("data_file.json") as f:
    data=json.load(f)

df=pd.DataFrame(data)
duckdb.register("data_table",df)

llm=OllamaLLM(model="llama3:8b")
schema=get_schema(data)
chat_history=[]
table_name="data_table"

while True:
    user_request=input("Enter your query ['exit' or 'quit' for ending session]: ")
    
    if user_request.lower() in ['exit','quit']:
        break
    
    conversation_history="/n".join(chat_history)
    prompt=PromptTemplate(
        input_variables=["conversation_history","user_request","schema","table_name"],
        template=PROMPT_TEMPLATE
    )

    chain=prompt|llm
    response=chain.invoke({
                    "conversation_history":conversation_history,
                    "user_request":user_request,
                    "schema":schema,
                    "table_name":table_name
                    })
    print("Ganerated response: " + response)
    response=extract_sql_query(response)
    duckdb.sql(response).show()
    chat_history.append(f"User:{user_request}")
    chat_history.append(f"Assistant:{response}")
