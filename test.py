from datetime import datetime, timedelta
today = datetime.today()
#today = f'{today.year}-{today.month}-{today.day}'
past_5_years = today - timedelta(days=5*365)
print(past_5_years)