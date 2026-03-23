from typing import Any, Dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from graph.state import GraphState


llm = ChatOpenAI(temperature=0)

generate_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant for retrieval-augmented question answering. "
            "Use the provided context to answer the question. If the context is "
            "insufficient, say so briefly and provide the best possible answer.",
        ),
        ("human", "Question: {question}\n\nContext:\n{context}"),
    ]
)

rag_chain = generate_prompt | llm | StrOutputParser()


def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    context = "\n\n".join([doc.page_content for doc in documents])
    generation = rag_chain.invoke({"question": question, "context": context})

    return {
        "documents": documents,
        "question": question,
        "generation": generation,
    }