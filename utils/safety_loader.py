import pandas as pd

def load_safety_info():
    try:
        df = pd.read_excel("data/women_safety.xlsx")  # Make sure this file exists
        grouped = df.groupby("category")

        safety_info = []
        for category, group in grouped:
            for _, row in group.iterrows():
                safety_info.append({
                    "category": category,
                    "detail": row["detail"]
                })
        return safety_info
    except Exception as e:
        print(f"[❌] Failed to load safety info: {e}")
        raise
