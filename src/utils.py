def convert_to_iso(date):
    if isinstance(date, str):
        from dateutil import parser
        return parser.parse(date).isoformat()
    return date.isoformat()

def get_default_dates():
    from datetime import datetime, timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    return start_date.isoformat(), end_date.isoformat()

def parse_relative_date(relative_date):
    from datetime import datetime, timedelta
    today = datetime.now()
    if "last year" in relative_date:
        return today - timedelta(days=365)
    elif "last quarter" in relative_date:
        return today - timedelta(days=90)
    elif "previous month" in relative_date:
        return today - timedelta(days=30)
    # Add more relative date parsing as needed
    return today

def format_dates(start_date, end_date):
    return convert_to_iso(start_date), convert_to_iso(end_date)