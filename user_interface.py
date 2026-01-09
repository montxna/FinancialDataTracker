from tkinter import *
from tkinter import ttk, messagebox
from data_analysis import DataAnalysis
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import smtplib

data = DataAnalysis()


class UserInterface:
    '''This class manages the user interface made in TKinter, and the adjacent windows'''
    def __init__(self):
        self.window = ttkb.Window(themename="superhero")
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
        if data.get_quote() != []:
            '''This function opens the stocks window'''
            StockViewWindow(self.window, data)
        else:
            messagebox.showerror("Error", "Please enter your financial data first!")
    def add_stocks(self):
        '''This function opens the window to add, edit or remove actives'''
        if data.get_quote() == []:
            messagebox.showwarning("Warning", "Your actives list is empty. Please enter your financial data first!")
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
                try:
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
                except KeyError:
                    pass

        treeview.grid(row=0, column=0, columnspan=2, padx=10, pady=10)





class StockEditorWindow(Toplevel):
    def __init__(self, master, data_controller):
        super().__init__(master)
        self.data = data_controller
        self.title("Stock Editor")
        self.list_of_finance = data.get_list()
        try:
            self.list_of_stocks = self.list_of_finance[0]
            self.list_of_crypto = self.list_of_finance[1]
        except IndexError:
            self.list_of_stocks = []
            self.list_of_crypto = []
        self.actives_list = ["Stocks", "Crypto"]
        self._setup_ui()
    def _setup_ui(self):
        self.combobox = ttk.Combobox(self, values=self.actives_list, state="readonly")
        self.combobox.set("Select an active")
        self.combobox.pack(pady=10, padx=10)
        self.button = Button(self, text="Show Selection", command=self.show_actives)
        self.button.pack(pady=10, padx=10)
        self.add_button = Button(self, text = "Add an active", command=self.add_active)
        self.add_button.pack(pady=10, padx=10)
        self.listbox = Listbox(self)
        self.listbox.pack(pady=10, padx=10)
        self.listbox.bind("<Button-3>", self.popup)
        self.popup_menu = Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Delete", command=self.delete_selected)


    def popup(self, event):
        if self.listbox.curselection():
            try:
                self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
            finally:
                self.popup_menu.grab_release()



    def add_active(self):
        """AICI TREBUIE SA FAC UN WINDOW PESTE STOCKEDITOR CU ACELEASI ELEMENTE, COMBO,LIST DE UNDE SE VOR LUA
        ELEMENTELE DIN POSSIBLE ACTIVES PENTRU STOCKS SI CRYPTO, LA ALEGERE SE ADAUGA IN LIST OF FINANCE, SE VERIFICA
        IN PREALABIL DACA SUNT DEJA IN LIST OF FINANCE, ASTFEL NU LE MAI DAU APPEND IN LISTBOX"""
        self.add_toplevel = Toplevel(self)
        self.add_toplevel.title("Add an Active")
        self.listpos = data.read_possible_finance()
        self.list_of_stocksadd = self.listpos[0]
        self.list_of_cryptoadd = self.listpos[1]
        self.comboboxadd = ttk.Combobox(self.add_toplevel, values=self.actives_list, state="readonly")
        self.comboboxadd.set("Select an active")
        self.comboboxadd.pack(pady=10, padx=10)
        self.buttonshow = Button(self.add_toplevel, text="Show Selection", command=self.show_actives_pos)
        self.buttonshow.pack(pady=10, padx=10)
        self.listboxadd = Listbox(self.add_toplevel)
        self.listboxadd.pack(pady=10, padx=10)
        self.buttonadd = Button(self.add_toplevel, text="Add", command=self.modify_list)
        self.buttonadd.pack(pady=10, padx=10)



    def modify_list(self):
        self.itemtoadd = self.listboxadd.get(self.listboxadd.curselection())
        self.activetoadd = self.comboboxadd.get()
        if self.activetoadd == "Stocks":
            self.list_of_stocks.append(self.itemtoadd)
        elif self.activetoadd == "Crypto":
            self.list_of_crypto.append(self.itemtoadd)
        data.add_item(self.list_of_stocks, self.list_of_crypto)
        messagebox.showinfo(title="Success", message="The active has been successfully added.")

    def delete_selected(self):
        item_to_remove = self.listbox.get(self.listbox.curselection())
        data.remove_item(item_to_remove)
        data.refresh_lists()
        self.list_of_finance = data.get_list()
        self.list_of_stocks = self.list_of_finance[0]
        self.list_of_crypto = self.list_of_finance[1]

        data.get_list()

        self.show_actives()
        messagebox.showinfo(title="Success", message="The active has been successfully deleted.")
    def show_actives(self):
        self.listbox.delete(0, END)
        option = self.combobox.get()
        if option == "Stocks":
            list = self.list_of_stocks
        elif option == "Crypto":
            list = self.list_of_crypto
        try:
            for item in list:
                self.listbox.insert(END, item)
        except UnboundLocalError:
            pass

    def show_actives_pos(self):
        self.listboxadd.delete(0, END)
        option = self.comboboxadd.get()
        if option == "Stocks":
            list = self.list_of_stocksadd
        elif option == "Crypto":
            list = self.list_of_cryptoadd
        try:
            for item in list:
                if item not in self.list_of_crypto and item not in self.list_of_stocks:
                    self.listboxadd.insert(END, item)
        except UnboundLocalError:
            pass

