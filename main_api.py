# from fastapi import FastAPI
# import subprocess

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Python AI server running"}

# @app.post("/generate")
# def generate(prompt: str):

#     result = subprocess.run(
#         ["ollama", "run", "llama3", prompt],
#         capture_output=True,
#         text=True
#     )

#     return {"response": result.stdout}

# from fastapi import FastAPI
# from vector import retriever
# import subprocess

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Python AI server running"}

# @app.post("/generate")
# def generate(prompt: str):

#     # Retrieve relevant ML document chunks
#     docs = retriever.invoke(prompt)

#     context = "\n\n".join([doc.page_content for doc in docs])

#     # Debug: show retrieved text in terminal
#     print("\n--- Retrieved Context ---")
#     print(context[:500])
#     print("-------------------------\n")

#     final_prompt = f"""
# Answer the question using the context below.

# Context:
# {context}

# Question:
# {prompt}
# """

#     result = subprocess.run(
#         ["ollama", "run", "llama3", final_prompt],
#         capture_output=True,
#         text=True
#     )

#     return {
#         "response": result.stdout,
#         "context_used": context[:300]   # optional debugging
#     }

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

model = OllamaLLM(model="llama3.2")

template = """
You are a helpful AI assistant.

Use the context below to answer the question.
If the answer is not in the context, say "I don't have enough information."

Context:
{context}

Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


@app.get("/")
def home():
    return {"message": "Python AI server running"}


@app.post("/generate")
def generate(data: PromptRequest):

    question = data.prompt

    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    result = chain.invoke({
        "context": context,
        "question": question
    })

    return {"response": result}