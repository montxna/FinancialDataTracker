import os
import requests
import csv
import pandas as pd
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

TWELVEDATA_KEY = os.environ.get("TWELVEDATA_KEY")
TWELVEDATA_QUOTE = "https://api.twelvedata.com/quote"

class DataAnalysis():
    def __init__(self):
        self.list_of_finance = []
        with open("list_of_finance.csv") as csvfile:
            self.reader = csv.reader(csvfile)
            for row in self.reader:
                self.list_of_finance.append(row[0])
        print(self.list_of_finance)
    def get_quote(self):
        list_of_data = []
        for item in self.list_of_finance:
            self.twelvedata_params = {
                "symbol": str(item),
                "apikey": TWELVEDATA_KEY,
            }
            response = requests.get(url = TWELVEDATA_QUOTE, params = self.twelvedata_params)
            data = response.json()
            data["timestamp"] = str(pd.to_datetime(data["timestamp"], unit = "s"))
            list_of_data.append(data)
        return list_of_data




