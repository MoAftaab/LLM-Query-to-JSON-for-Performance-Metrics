import json
from datetime import datetime, timedelta
from llm_integration import query_llm
from query_parser import parse_query

def main():
    conversation_history = []
    previous_data = None
    while True:
        user_query = input("Enter your query about company performance metrics (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        
        # Parse the user query to extract relevant information
        parsed_data = parse_query(user_query, previous_data)
        
        if not parsed_data:
            print("Could not extract information from the query.")
            continue
        
        previous_data = parsed_data
        
        # Prepare the structured JSON output
        output_json = json.dumps(parsed_data, indent=2)
        
        # Print the structured JSON response
        print("Structured JSON Output:")
        print(output_json)
        
        # Call the LLM for further processing
        try:
            llm_response = query_llm(conversation_history, user_query)
            print("LLM Response:")
            print(llm_response)
        except Exception as e:
            print(f"Failed to handle query: {e}")

if __name__ == "__main__":
    main()