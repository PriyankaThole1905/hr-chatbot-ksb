from langchain_community.document_loaders import PyMuPDFLoader
import os

def load_all_pdfs():
    loader1 = PyMuPDFLoader(r"C:\Users\AIUSER\HR_Chatbot-2\docs\PDFContent.pdf")
    loader2 = PyMuPDFLoader(r"C:\Users\AIUSER\HR_Chatbot-2\docs\SERVICE MILESTONE RECOGNITION POLICY_R1.pdf")
    return loader1.load() + loader2.load()


