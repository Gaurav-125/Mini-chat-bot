from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """


Here are some relevant reviews:
{reviews}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n-------------------------")
    question = input("Ask question (q to quit): ")

    if question.lower() == "q":
        break

    docs = retriever.invoke(question)

    reviews = "\n\n".join([doc.page_content for doc in docs])

    result = chain.invoke({
        "reviews": reviews,
        "question": question
    })

    print("\nAnswer:\n", result)