import requests
from datetime import *
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

now = datetime.now()

previous_Date = datetime.today() - timedelta(days=1)
previous_date = previous_Date.strftime("%Y-%m-%d")

two_previous_Date = datetime.today() - timedelta(days=2)
two_previous_date = two_previous_Date.strftime("%Y-%m-%d")

stock_api_key = "REPLACE"

stock_paramaters = {
    "function" : "TIME_SERIES_INTRADAY",
    "symbol" : STOCK,
    "interval" : "60min",
    "apikey" : stock_api_key,
}

stock_data = requests.get(url="https://www.alphavantage.co/query", params=stock_paramaters)
stock_data.raise_for_status()
print(stock_data.json())
previous_day_stock = stock_data.json()["Time Series (60min)"][f"{previous_date} 20:00:00"]["4. close"]
two_previous_day_stock = stock_data.json()["Time Series (60min)"][f"{two_previous_date} 20:00:00"]["4. close"]

increase = float(previous_day_stock) - float(two_previous_day_stock)
per_increase = float(increase) / float(two_previous_day_stock) * 100
change = round(per_increase, 2)


news_api_key = "REPLACE"

news_parmaters = {
    "q" : COMPANY_NAME,
    "from" : two_previous_date,
    "sortBy" : "popularity",
    "apikey" : news_api_key,
}
if change > 5:
    news_data = requests.get(url="https://newsapi.org/v2/everything", params=news_parmaters)
    news_data.raise_for_status()

    if previous_day_stock > two_previous_day_stock:
        direction = "Up"
    else:
        direction = "Down"

    my_email = "REPLACE@gmail.com"
    password = "REPLACE"

    for _ in range(3):
        a = news_data.json()["articles"][_]["title"]
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="REPLACE@gmail.com", msg=f"Subject: {STOCK}: {direction} {change}%\n\n{a} ")