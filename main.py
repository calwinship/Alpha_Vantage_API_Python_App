import tkinter as tk
from tkinter import ttk
from decouple import config
import requests

# Constants
API_KEY = config('ALPHA_VANTAGE_API_KEY')
BASE_URL = "https://www.alphavantage.co/query"

# Fetch the stock data
def fetch_stock_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Error Message" in data:
        return f"Error fetching data for {symbol}"

    last_refreshed = data["Meta Data"]["3. Last Refreshed"]
    last_close = data["Time Series (Daily)"][last_refreshed]["4. close"]

    return f"Stock: {symbol}\nLast Refreshed: {last_refreshed}\nClosing Price: ${last_close}"

# On button click
def on_fetch():
    symbol = stock_symbol_entry.get()
    if not symbol:
        result_label["text"] = "Please enter a stock symbol."
        return

    result_label["text"] = "Fetching data..."
    stock_data = fetch_stock_data(symbol)
    result_label["text"] = stock_data

# GUI
root = tk.Tk()
root.title("Stock Data Fetcher")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

stock_symbol_label = ttk.Label(frame, text="Enter Stock Symbol:")
stock_symbol_label.grid(row=0, column=0, sticky=tk.W, pady=5)

stock_symbol_entry = ttk.Entry(frame)
stock_symbol_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

fetch_button = ttk.Button(frame, text="Fetch Data", command=on_fetch)
fetch_button.grid(row=2, column=0, pady=20)

result_label = ttk.Label(frame, text="")
result_label.grid(row=3, column=0, pady=5)

root.mainloop()