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
        csvfile = pd.read_csv("list_of_finance.csv", header=None)
        self.list_of_finance.append(csvfile[0].tolist())
        self.list_of_finance.append(csvfile[1].tolist())
        print(self.list_of_finance)
    def get_quote(self):
        list_of_data = []

        for row in self.list_of_finance:
            row_list = []

            for symbol in row:
                self.twelvedata_params = {
                    "symbol": symbol,
                    "apikey": TWELVEDATA_KEY,
                }

                response = requests.get(url = TWELVEDATA_QUOTE, params = self.twelvedata_params)
                data = response.json()
                #Converts timestamp from Unix to a date
                data["timestamp"] = str(pd.to_datetime(data["timestamp"], unit = "s"))
                row_list.append(data)

            list_of_data.append(row_list)
        return list_of_data




