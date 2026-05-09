from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import os

# folder containing PDFs
PDF_FOLDER = "./pdfs"

# database location
DB_LOCATION = "./chroma_langchain_db"

# faster embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# text splitter for large PDFs
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=40
)

# check if database already exists
if not os.path.exists(DB_LOCATION):

    print("Creating vector database...")

    documents = []

    # load all pdfs
    for file in os.listdir(PDF_FOLDER):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(PDF_FOLDER, file)
            reader = PdfReader(pdf_path)

            for page_num, page in enumerate(reader.pages):

                text = page.extract_text()

                if not text:
                    continue

                chunks = text_splitter.split_text(text)

                for chunk in chunks:

                    doc = Document(
                        page_content=chunk,
                        metadata={
                            "source": file,
                            "page": page_num + 1
                        }
                    )

                    documents.append(doc)

    # batch insertion (fast)
    vector_store = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=DB_LOCATION
    )

    print("Vector database created successfully!")

else:

    print("Vector database already exists. Loading...")

    vector_store = Chroma(
        persist_directory=DB_LOCATION,
        embedding_function=embeddings
    )

# retriever used in main.py
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)