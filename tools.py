from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

def saveToTxt (data:str, filename:str ="research_out_txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8" )as f:
        f.write(formatted_text)

        return f"Data sucessfully saved to{filename}"

save_Tool = Tool(
    name="save_text_to_file",
    func=saveToTxt,
    description="Saves structured research data to text file"
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search_Web",
    func=search.run,
    description="Search the web for information"
)

api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=150, lang="en")
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
