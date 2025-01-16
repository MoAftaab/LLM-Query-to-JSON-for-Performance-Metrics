import os
import requests
from dotenv import load_dotenv
import re
from datetime import datetime, timedelta
import logging

# Load environment variables from .env file
load_dotenv()

# Set up your API credentials
API_KEY = os.getenv('LLM_API_KEY')
MODEL_NAME = "llama-3.1-8b-instant"
API_URL = f"https://api.groq.com/openai/v1/chat/completions"  # Correct API URL

# Set up logging
logging.basicConfig(level=logging.INFO)

def query_llm(conversation_history: list, query: str) -> str:
    # Function to send a query to the LLM and receive a response
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    conversation_history.append({'role': 'user', 'content': query})
    payload = {
        'model': MODEL_NAME,
        'messages': conversation_history
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    
    try:
        response_json = response.json()
        conversation_history.append(response_json['choices'][0]['message'])
        return response_json['choices'][0]['message']['content']
    except requests.exceptions.JSONDecodeError:
        print("Error: Unable to decode JSON response")
        print("Response content:", response.text)
        raise
    
def extract_information(llm_response: str) -> dict:
    """
    Function to extract structured information from the LLM response.
    """
    metric_mapping = {
        "gmv": "GMV",
        "revenue": "Revenue",
        "profit": "Profit",
        "sales": "Sales",
        "growth": "Growth"
    }

    # Extract entities and metrics
    entities = re.findall(r"(Flipkart|Amazon|Google|Microsoft|Apple)", llm_response, re.IGNORECASE)
    parameter_match = re.search(r"(gmv|revenue|profit|sales|earnings|growth)", llm_response, re.IGNORECASE)
    parameter = metric_mapping.get(parameter_match.group(0).lower(), "Unknown")

    # Extract dates
    today = datetime.today()
    start_date = (today - timedelta(days=365)).date().isoformat()
    end_date = today.date().isoformat()

    start_date_match = re.search(r"from (\d{4}-\d{2}-\d{2})", llm_response)
    end_date_match = re.search(r"to (\d{4}-\d{2}-\d{2})", llm_response)

    if start_date_match:
        start_date = start_date_match.group(1)
    if end_date_match:
        end_date = end_date_match.group(1)

    # Construct the structured data
    extracted_data = []
    for entity in entities:
        extracted_data.append({
            "entity": entity,
            "parameter": parameter,
            "startDate": start_date,
            "endDate": end_date
        })
    
    return extracted_data

def handle_query(query: str) -> dict:
    """
    Main function to handle the user query and return structured JSON data.
    """
    # Ensure that query_llm is called with a single argument (query)
    llm_response = query_llm(query)
    structured_data = extract_information(llm_response)
    return structured_data

if __name__ == "__main__":
    # Input query from the user
    user_query = input("Enter your query about company performance metrics: ")
    
    try:
        result = handle_query(user_query)
        print("Structured JSON Output:")
        print(result)
    except Exception as e:
        print(f"Failed to handle query: {e}")
