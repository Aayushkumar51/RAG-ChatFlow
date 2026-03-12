from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv


load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

def get_llm_chain(retriever):

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        # Updated to a currently supported Groq model
        model_name="llama-3.3-70b-versatile",
    )
    
    prompt=PromptTemplate(
        input_variables=["context","input"],
        template="""
        You are an AI Medical Assistant designed to provide helpful and safe medical information.

        Use ONLY the information provided in the context below to answer the user's question.

        Context:
        {context}

        User Question:
        {input}

        Instructions:
        1. Answer the question clearly using the provided context.
        2. Do not make up information that is not in the context.
        3. If the answer is not found in the context, say:
        "I could not find relevant medical information in the provided documents."
        4. Provide a concise and easy-to-understand explanation.
        5. If the question relates to symptoms or treatment, suggest consulting a qualified healthcare professional.
        6. Do NOT provide definitive diagnoses.







        """
        


    )

    document_chains = create_stuff_documents_chain(llm=llm, prompt=prompt)

    retriever_chain = create_retrieval_chain(retriever, document_chains)

    return retriever_chain