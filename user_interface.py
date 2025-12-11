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
        '''This function opens the stocks window'''
        StockViewWindow(self.window, data)
    def add_stocks(self):
        '''This function opens the window to add, edit or remove actives'''
        StockEditorWindow(self.window,data)

    def add_edit_mail(self):
        pass

class StockViewWindow(Toplevel):
    def __init__(self, master, data_analysis):
        super().__init__(master)
        self.data = data_analysis
        self.response = data.get_quote()
        self.title("Financial Data")
        self._setup_ui()

    def _setup_ui(self):
        treeview = ttk.Treeview(self, style="BW.TLabel",
                                columns=("Name", "Currency", "Date", "Open", "Close",
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

        self.stocks_level = treeview.insert('', 'end', text="Stocks")
        self.crypto_level = treeview.insert('', 'end', text="Crypto")

        categories = [
            (self.response[0], self.stocks_level),
            (self.response[1], self.crypto_level),
        ]

        treeview.tag_configure('priceUp', foreground='green')
        treeview.tag_configure('priceDown', foreground='red')

        for data_list, node_level in categories:
            for item in data_list:
                usedTag = "priceUp" if float(item['percent_change']) > 0 else "priceDown"

                treeview.insert(node_level, 'end', text=item["symbol"], values=(f"{item['name']}",
                                                                                f"{item.get('currency', 'USD')}",
                                                                                f"{item['datetime']}",
                                                                                f"{item['open']}",
                                                                                f"{item['close']}",
                                                                                f"{item['percent_change']}",
                                                                                f"{item['fifty_two_week']["high"]}",
                                                                                f"{item['fifty_two_week']["low"]}"),
                                tags=f"{usedTag}")

        treeview.grid(row=0, column=0, columnspan=2, padx=10, pady=10)





class StockEditorWindow(Toplevel):
    def __init__(self, master, data_controller):
        super().__init__(master)
        self.data = data_controller
        self.title("Stock Editor")
        self.list_of_finance = data.get_list()
        self.list_of_stocks = self.list_of_finance[0]
        self.list_of_crypto = self.list_of_finance[1]
        self.actives_list = ["Stocks", "Crypto"]
        self._setup_ui()
    def _setup_ui(self):
        self.combobox = ttk.Combobox(self, values=self.actives_list, state="readonly")
        self.combobox.set("Select an active")
        self.combobox.pack(pady=10, padx=10)
        self.button = ttk.Button(self, text="Show Selection", command=self.show_actives)
        self.button.pack(pady=10, padx=10)
        self.listbox = Listbox(self)
        self.listbox.pack(pady=10, padx=10)








    def show_actives(self):
        self.listbox.delete(0, END)
        option = self.combobox.get()
        if option == "Stocks":
            for item in self.list_of_stocks:
                self.listbox.insert(END, item)
        elif option == "Crypto":
            for item in self.list_of_crypto:
                self.listbox.insert(END, item)



