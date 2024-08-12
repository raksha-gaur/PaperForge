import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint

load_dotenv()


def load_llm():
    model_name = 'mistralai/Mistral-7B-Instruct-v0.2'
    token = os.getenv('HUGGINGFACEHUB_API_TOKEN')

    # Debugging: Print the token
    print(f"Using token: {token}")
    llm = HuggingFaceEndpoint(repo_id=model_name, max_new_tokens=2000, temperature=0.7, huggingfacehub_api_token=token)

    return llm


def get_llm_response(vectorstore, prompt):
    llm = load_llm()

    # Retrieve the context from the vector store
    retriever = vectorstore.as_retriever(search_kwargs={'k': 2000})
    docs = retriever.invoke(prompt)
    context = "\n".join([doc.page_content for doc in docs])

    final_prompt = f"""context:{context}\n{prompt}"""
    # Generate the final response using the LLM
    response = llm.invoke(final_prompt)
    return response
