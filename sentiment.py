
import requests
from datetime import datetime,timedelta
import google_sheets  # Your separate module

SHEET_ID = "1YkTXNX5LAhANICxzu4Tj4Hr6aFMoXdufH_ev1gmRx7c"
WORKSHEET_NAME = "SEMENT"

def get_sentiment_for_ticker(ticker):
    url = "https://api.marketaux.com/v1/news/all"
    params = {
        "api_token": "GHvX2fU3SlWfely31ktchdIGv7bGqVVr0AhGQwpC",
        "symbols": ticker
    }

    response = requests.get(url, params=params)
    data = response.json()

    sentiments = []
    if "data" in data:
        for article in data["data"]:
            entities = article.get("entities", [])
            for e in entities:
                if e.get("symbol") == ticker and "sentiment_score" in e:
                    sentiments.append(e["sentiment_score"])
    
    
    if sentiments:
        sum_sentiment=0
        length=0
        for i in sentiments:
            if i:
                sum_sentiment+=i
                length+=1
            
        avg_sentiment = sum_sentiments / length
        
        if avg_sentiment > 0:
            sentiment_label = "Positive"
        elif avg_sentiment < 0:
            sentiment_label = "Negative"
        elif (None in sentiments):
            sentiment_label = "None"
        else:
            sentiment_label = "Neutral"
        return round(avg_sentiment, 4), sentiment_label
    else:
        return None, None

def main():
    tickers = ["^NSEI", "^NSEBANK"]
    print_ticker=["NIFTY","NIFTY_BANK"]
    headers = ["NSE", "SENTIMENT_SCORE", "SENTIMENT",]
    rows = []

    # Get sentiment data
    for ticker in tickers:
        sentiment_score, sentiment_label = get_sentiment_for_ticker(ticker)
        if sentiment_score is not None:
            rows.append([print_ticker, sentiment_score, sentiment_label])
        else:
            rows.append([print_ticker, "NO DATA FOUND", "NO DATA FOUND"])

    # Append rows to Google Sheet
    google_sheets.update_google_sheet_by_name(SHEET_ID, WORKSHEET_NAME, headers, rows)

    #Convert GMT time to IST
    gmt_time=datetime.utcnow()
    ist_time=gmt_time+timedelta(hours=5,minutes=30)
    
    # Append timestamp as a separate row at the end
    now = ist_time.strftime("%Y-%m-%d %H:%M:%S")
    google_sheets.append_footer(SHEET_ID, WORKSHEET_NAME, [now])

if __name__ == "__main__":
    main()
