# tools/db_tools.py
from langchain.chat_models import ChatOpenAI
from langchain import SQLDatabase
from langchain.chains import SQLDatabaseChain




class BaseDBTool:
    """Wrapper around a SQLite DB + SQLDatabaseChain for natural-language to SQL."""


def __init__(self, db_path: str, llm=None, table_name: str = None):
    self.db_uri = f"sqlite:///{db_path}"
    self.db = SQLDatabase.from_uri(self.db_uri)
    self.llm = llm or ChatOpenAI(temperature=0)
    # SQLDatabaseChain will ask the model to generate SQL and run it against the DB.
    self.chain = SQLDatabaseChain.from_llm(self.llm, self.db, verbose=False)
    self.table_name = table_name


def run(self, natural_language_query: str) -> str:
    # Optionally prefix the question to guide LLM towards the right table
    if self.table_name:
        prompt = (
        f"You are querying the table `{self.table_name}` in a sqlite database. "
        f"Answer the user using data from the table. If the question cannot be answered from the table, say so.\nQuestion: {natural_language_query}"
        )
    else:
        prompt = natural_language_query


    # Use SQLDatabaseChain to convert NL -> SQL -> run -> return result (as text)
    return self.chain.run(prompt)


class HeartDiseaseDBTool(BaseDBTool):
    def __init__(self, db_path: str, llm=None):
        super().__init__(db_path, llm=llm, table_name="heart_disease")


class CancerDBTool(BaseDBTool):
    def __init__(self, db_path: str, llm=None):
        super().__init__(db_path, llm=llm, table_name="cancer")

class DiabetesDBTool(BaseDBTool):
    def __init__(self, db_path: str, llm=None):
        super().__init__(db_path, llm=llm, table_name="diabetes")