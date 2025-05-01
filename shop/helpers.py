from django.utils import timezone
from datetime import datetime, timedelta

def get_current_and_previous_days():
    #TODO Add documentation
    ''''''
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_current_month = today.replace(day=1)

    # Start of previous month
    if start_of_current_month.month == 1:
        start_of_prev_month = start_of_current_month.replace(year=start_of_current_month.year - 1, month=12)
    else:
        start_of_prev_month = start_of_current_month.replace(month=start_of_current_month.month - 1)

    # End of previous month = one second before current month starts
    end_of_prev_month = start_of_current_month - timedelta(seconds=1)
    
    return start_of_prev_month, end_of_prev_month, start_of_current_month

def get_sales_rate(prev, curr):
    #TODO Add documentation
    # Avoid division by zero and handle edge cases
    rate_change = 0
    if prev == 0:
        if curr > 0:
            rate_change = 100.0  # Full increase from nothing
        else:
            rate_change = 0.0    # No sales in either month
    else:
        rate_change = ((curr - prev) / prev) * 100
        
    rate_class = "text-muted"
    if rate_change > 0:
        rate_class = "text-success"
    elif rate_change < 0:
        rate_class = "text-danger"

    return rate_change, rate_class
