import os
from groq import Groq

def analyze_sprint(summary_data, model="llama-3.1-8b-instant"):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""
    You are an expert Sprint Analyst. Using the list of sprint items below, create actionable insights.
    DATA:
    {summary_data}
    Provide JSON output:
    - High-Risk Items
    - Dependencies & Blockers
    - Recommended Execution Order
    - 10-Day Plan
    """
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an agile sprint planning assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content.strip()
