import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from app.db.vector_store import query_documents
from app.config import settings

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0.7
)

prompt = ChatPromptTemplate.from_template("""
You are an expert sports betting analyst. 
Use the following context retrieved from our sports database to answer the question.
Be analytical, specific, and highlight key factors that could influence the betting outcome.
If the context doesn't contain enough information, say so clearly.

Context:
{context}

Question:
{question}

Provide a detailed betting analysis:
""")

chain = prompt | llm | StrOutputParser()

def analyze_query(query: str) -> str:
    try:
        logger.info(f"Analyzing query: {query}")

        context_docs = query_documents(query_text=query, n_results=5)

        if not context_docs:
            logger.warning("No context found in vector store for query")
            return "I don't have enough data to analyze this query. Try ingesting some match data first."

        context = "\n".join(context_docs)

        response = chain.invoke({
            "context": context,
            "question": query
        })

        return response

    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        return "An error occurred during analysis. Please try again."