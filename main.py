from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_Tool


load_dotenv()
# llm = ChatOpenAI(model="gpt-4.5-turbo")
# response = llm.invoke("Hello, how are you?")
# print(response)

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatAnthropic(model="claude-3-7-sonnet-20250224")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
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

tools=[search_tool, wiki_tool, save_Tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
    )

agent_executor = AgentExecutor(agent=agent,tools=tools, verbose=True)
query = input("How can i assist you with 🙂?")
raw_response = agent_executor.invoke({"query": query})

try:
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error while parsing response", e, "raw_response:", raw_response)
