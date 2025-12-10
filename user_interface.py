from tkinter import *
from tkinter import ttk
from data_analysis import DataAnalysis
import smtplib

data = DataAnalysis()


class UserInterface:
    '''This class manages the user interface made in TKinter, and the adjacent windows'''
    def __init__(self):
        self.window = Tk()
        self.window.title("Financial Data Tracker")

        self.style = ttk.Style()
        self.style.configure("BW.TLabel", foreground="black", background="light gray")
        self.style.configure('TButton', font=("calibri", 20, "bold"), borderwidth=2, cursor="hand2")
        self.style.map('TButton', foreground = [('active', '!disabled', 'green')],
                     background = [('active', 'black')])

        self.l1 = ttk.Label(text="Welcome to my financial data tracker!", style="BW.TLabel", compound="center", font=("Arial", 20))
        self.l1.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.view_stock_button = ttk.Button(self.window, text="View Your Financial Data")
        self.view_stock_button.configure(command=self.open_stocks)
        self.view_stock_button.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.add_stock_button = ttk.Button(self.window, text="Add your Financial Data")
        self.add_stock_button.configure(command=self.add_stocks)
        self.add_stock_button.grid(row=1, column=1, padx=10, pady=10)

        self.add_mail_button = ttk.Button(self.window, text="Add/Edit Your Email Address")
        self.add_mail_button.configure(command=self.add_edit_mail)
        self.add_mail_button.grid(row=1, column=2, padx=10, pady=10)

        self.window.mainloop()



    def open_stocks(self):
        self.response = data.get_quote()
        self.stock_window = Toplevel(self.window)
        self.stock_window.title("Stock Data")
        treeview = ttk.Treeview(self.stock_window, style="BW.TLabel", columns=("Name", "Currency", "Date", "Open","Close",
                                                                               "Percent Change", "Yearly High", "Yearly Low"))
        treeview.heading("#0", text="Symbol")
        treeview.heading("Name", text="Name")
        treeview.heading("Currency", text="Currency")
        treeview.heading("Date", text="Date")
        treeview.heading("Open", text="Open")
        treeview.heading("Close", text="Close")
        treeview.heading("Percent Change", text="Percent Change")
        treeview.heading("Yearly High", text="Yearly High")
        treeview.heading("Yearly Low", text="Yearly Low")

        self.first_level = treeview.insert('', 'end', text="My Financial Actives")

        treeview.tag_configure('priceUp', foreground='light green')
        treeview.tag_configure('priceDown', foreground='red')

        for item in self.response:
            if float(item['percent_change']) > 0:
                usedTag = "priceUp"
            else:
                usedTag = "priceDown"
            treeview.insert(self.first_level, 'end', text=item["symbol"], values=(f"{item['name']}",f"{item.get('currency', 'USD')}", f"{item['datetime']}", f"{item['open']}",
                                                                                  f"{item['close']}",f"{item['percent_change']}",
                                                                                  f"{item['fifty_two_week']["high"]}",f"{item['fifty_two_week']["low"]}"), tags=f"{usedTag}")


        treeview.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        pass
    def add_stocks(self):
        pass
    def add_edit_mail(self):
        pass