import sys
import json
import yfinance as yf

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Fetching historical data or info summary
        info = stock.info
        info_keys = list(stock.info.keys())
        for key in sorted(info_keys):
            print(key)
       # data = {
       #     "Officers": info.get("companyOfficers"),
       # }

       # print(json.dumps(data))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    # Pass the ticker symbol as a command line argument
    if len(sys.argv) > 1:
        get_stock_data(sys.argv[1])