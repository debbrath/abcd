# main_agent.py
# assemble everything
# main_agent.py
import os
from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType


from tools.db_tools import HeartDiseaseDBTool, CancerDBTool, DiabetesDBTool
from tools.web_search_tool import MedicalWebSearchTool




def make_tools():
    llm = ChatOpenAI(temperature=0)
    heart = HeartDiseaseDBTool("heart_disease.db", llm=llm)
    cancer = CancerDBTool("cancer.db", llm=llm)
    diabetes = DiabetesDBTool("diabetes.db", llm=llm)
    web = MedicalWebSearchTool(
        serpapi_key=os.getenv("SERPAPI_API_KEY"),
        bing_api_key=os.getenv("BING_API_KEY"),
    )

    tools = [
        Tool(
            name="HeartDiseaseDBTool",
            func=lambda q, tool=heart: tool.run(q),
            description="Use for queries about heart disease dataset: counts, averages, distributions, statistics, column-specific questions.",
        ),
        Tool(
            name="CancerDBTool",
            func=lambda q, tool=cancer: tool.run(q),
            description="Use for queries about the cancer dataset: predictions, counts, correlations, statistics.",
        ),
        Tool(
            name="DiabetesDBTool",
            func=lambda q, tool=diabetes: tool.run(q),
            description="Use for queries about the diabetes dataset: values, distributions, numeric queries.",
        ),
        Tool(
            name="MedicalWebSearchTool",
            func=lambda q, tool=web: tool.search(q),
            description="Use for medical knowledge: definitions, symptoms, treatments, high-level medical facts. Should NOT be used for exact numeric statistics from the datasets.",
        ),
    ]
    return tools, llm


def is_data_question(question: str) -> bool:
     """Heuristic router: if question contains words relating to numbers/statistics/datasets, treat as DB query."""
     q = question.lower()
     stats_keywords = [
    "how many",
    "count",
    "percentage",
    "%",
    "average",
    "mean",
    "median",
    "std",
    "standard deviation",
    "distribution",
    "correlation",
    "correl",
    "rows",
    "records",
    "what is the number",
    "how often",
    "per",
  ] 
     dataset_keywords = ["heart", "cancer", "diabetes", "glucose", "cholesterol", "age", "blood pressure"]

     if any(k in q for k in stats_keywords + dataset_keywords):
      return True
     return False

def build_agent():
    tools, llm = make_tools()
    agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    )
    return agent


def run_interactive():
    agent = build_agent()
    print("Multi-tool Medical Agent — type 'exit' to quit")
    while True:
      q = input("User: ")
      if q.strip().lower() in ("exit", "quit"):
       break

      # Use heuristic routing to choose which tool to call. The agent also can decide.
      if is_data_question(q):
      # Let the agent with DB tools answer — agent will select the DB tool.
        resp = agent.run(q)
      else:
         # Force web search for definitions / symptoms / cures
            web_tool = [t for t in agent.tools if t.name == "MedicalWebSearchTool"][0]
            resp = web_tool.func(q)

            print("Agent:\n", resp)