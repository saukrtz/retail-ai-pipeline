import requests
import os

def debug_error():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set.")
        return
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    error_msg = "Error during cleaning: 'price'"
    code_snippet = """
def clean_data(df):
    try:
        logging.info("Starting data cleaning...")
        df = df.drop_duplicates()
        df['quantity'] = df['quantity'].fillna(1)
        df['price'] = df['price'].fillna(0)
        df['discount'] = df['discount'].fillna(0)
        df = df[(df['price'] > 0) & (df['quantity'] > 0)]
        logging.info(f"Cleaning complete. Remaining rows: {len(df)}")
        return df
    except Exception as e:
        logging.error(f"Error during cleaning: {e}")
        return None
    """
    
    prompt = f"""
    A retail data pipeline failed with the following error:
    {error_msg}
    
    The failing code section is:
    {code_snippet}
    
    Task:
    1. Explain why this happened.
    2. Provide an updated 'clean_data' function that handles missing columns gracefully (e.g., check if columns exist before filling or filtering).
    3. Return ONLY the updated Python function.
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        suggestion = response.json()['choices'][0]['message']['content']
        with open("debug_suggestion.txt", "w") as f:
            f.write(suggestion)
        print("AI Debugging suggestion saved to debug_suggestion.txt")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    debug_error()
