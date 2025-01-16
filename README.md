# LLM Performance Metrics Application

## Overview
The LLM Performance Metrics Application is designed to process user queries related to company performance metrics and convert them into a structured JSON format. It leverages the llama-3.1-8b-instant model for natural language understanding and extraction of relevant information.

## Project Structure
```
llm-performance-metrics-app
├── src
│   ├── main.py            # Entry point for the application
│   ├── llm_integration.py # Functions to interact with the LLM model
│   ├── query_parser.py    # Parses user queries and extracts information
│   └── utils.py           # Utility functions for date manipulation
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
└── notebook
    └── llm_performance_metrics.ipynb # Jupyter notebook for testing
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd llm-performance-metrics-app
   ```

2. **Install dependencies:**
   Ensure you have Python 3.7 or higher installed. Then, run:
   ```
   pip install -r requirements.txt
   ```

3. **Configure LLM API:**
   Set up your API credentials for the llama-3.1-8b-instant model in the `llm_integration.py` file.

## Usage
To run the application, execute the following command:
```
python src/main.py
```
You will be prompted to enter your query regarding company performance metrics.

### Example Queries
- "Get me Flipkart's GMV for the last one year."
- "Compare Amazon and Flipkart's revenue from last quarter."

## JSON Output Structure
The application will return the extracted information in the following JSON format:
```json
[
  {
    "entity": "<company_name>",
    "parameter": "<metric_name>",
    "startDate": "<start_date_iso>",
    "endDate": "<end_date_iso>"
  }
]
```

## Additional Notes
- The application handles default date values if not specified in the query.
- It supports multiple company comparisons in a single query.
- For testing and demonstration, refer to the Jupyter notebook located in the `notebook` directory.

## License
This project is licensed under the MIT License. See the LICENSE file for details.