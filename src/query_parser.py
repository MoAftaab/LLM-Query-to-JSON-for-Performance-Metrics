import re
from datetime import datetime, timedelta

def parse_query(query: str, previous_data=None):
    # Example regex to extract company names and metrics
    companies = re.findall(r'\b(Flipkart|Amazon|Walmart|Target)\b', query, re.IGNORECASE)
    metric = re.search(r'\b(GMV|revenue|profit)\b', query, re.IGNORECASE)
    
    # Extract dates from the query
    dates = re.findall(r'\b(\d{4}-\d{2}-\d{2})\b', query)
    
    # Handle relative date phrases like "last one year"
    if "last one year" in query.lower():
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        dates = [start_date.isoformat(), end_date.isoformat()]
    
    if not companies and previous_data:
        companies = [data['entity'] for data in previous_data]
        if "compare" in query.lower() or "this" in query.lower():
            companies.append("Amazon")  # Add Amazon for comparison if mentioned in follow-up query
    
    if not metric and previous_data:
        metric = re.search(r'\b(GMV|revenue|profit)\b', previous_data[0]['parameter'], re.IGNORECASE)
    
    if not companies or not metric:
        return None
    
    start_date = datetime.strptime(dates[0], '%Y-%m-%d').date().isoformat() if dates else previous_data[0]['startDate']
    end_date = datetime.strptime(dates[1], '%Y-%m-%d').date().isoformat() if dates else previous_data[0]['endDate']
    
    parsed_data = []
    for company in companies:
        parsed_data.append({
            "entity": company.capitalize(),
            "parameter": metric.group(0).lower(),
            "startDate": start_date,
            "endDate": end_date
        })
    
    return parsed_data