import os

import pandas
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
        try:
            self.csvfile = pd.read_csv("list_of_finance.csv", header=None)
            self.csvfile = self.csvfile.fillna("")
            self.list_of_finance.append(self.csvfile[0].tolist())
            self.list_of_finance.append(self.csvfile[1].tolist())
        except pandas.errors.EmptyDataError:
            pass
    def get_quote(self):
        list_of_data = []


        if self.list_of_finance != []:
            for row in self.list_of_finance:
                row_list = []

                for symbol in row:
                    self.twelvedata_params = {
                        "symbol": symbol,
                        "apikey": TWELVEDATA_KEY,
                    }

                    response = requests.get(url = TWELVEDATA_QUOTE, params = self.twelvedata_params)
                    response.raise_for_status()
                    data = response.json()
                    #Converts timestamp from Unix to a date
                    try:
                        data["timestamp"] = str(pd.to_datetime(data["timestamp"], unit = "s"))
                    except KeyError:
                        pass
                    row_list.append(data)

                list_of_data.append(row_list)
        return list_of_data

    def get_list(self):
        return self.list_of_finance

    def remove_item(self, item):
        self.csvfile = self.csvfile.replace(f"{item}", "")
        self.csvfile.to_csv("list_of_finance.csv", index = False, header = False)
        self.refresh_lists()


    def refresh_lists(self):
        self.list_of_finance = []
        self.csvfile = pd.read_csv("list_of_finance.csv", header=None)
        self.csvfile = self.csvfile.fillna("")
        self.list_of_finance.append(self.csvfile[0].tolist())
        self.list_of_finance.append(self.csvfile[1].tolist())



