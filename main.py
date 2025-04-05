from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent,AgentExecutor
from tools import search_tool,wiki_tool,save_tool
from langchain_core.output_parsers import JsonOutputParser


load_dotenv()




llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")




class ReasearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used:list[str]
    

parser = JsonOutputParser(pydantic_object=ReasearchResponse)


prompt=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


tools=[search_tool,wiki_tool,save_tool]
agent=create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executer= AgentExecutor(agent=agent,tools=tools,verbose=True)
query=input("What can i help you in research?")
raw_response=agent_executer.invoke({"query":query})



try:
    
    structured_response= parser.parse(raw_response['output'])
    for key, value in structured_response.items():
        print(f"\n{key.upper()}\n{'-' * len(key)}\n{value}")

    

except Exception as e:
    print("Error in parsing response",e,"Raw response -",raw_response)

