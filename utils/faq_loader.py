import pandas as pd

def load_faqs():
    df = pd.read_excel("data/faq.xlsx")  # Make sure this Excel file exists
    faqs = []
    for _, row in df.iterrows():
        faqs.append({"question": row["question"], "answer": row["answer"]})
    return faqs
