import fitz  # PyMuPDF
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document


def extract_text_from_pdf(pdf_file, start_page, end_page):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    extracted_text = ""
    for page_num in range(start_page - 1, end_page):
        page = pdf_document.load_page(page_num)
        extracted_text += page.get_text()
    return extracted_text


def create_vectorstore(text):
    documents = [Document(page_content=chunk) for chunk in text.split('\n') if chunk]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    print("vectorstore successfully created")
    return vectorstore
