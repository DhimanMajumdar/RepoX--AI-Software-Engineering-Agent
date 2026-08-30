from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm()->ChatGroq:
    return ChatGroq(
        model="groq/compound-mini",
        temperature=0
    )

    