from tkinter import *
from tkinter import messagebox as msgbox
from tkinter import ttk
from PIL import ImageTk, Image
import requests
import json
import os
import datetime
import pandas as pd

class stock():
    def __init__(self, root):
        root.title("Get Share Market Details ..")
        self.root = Frame(root,width=1000,height=600,bg="black")
        self.root.pack()
        self.list_indics = ["NIFTY 50",
                            "NIFTY NEXT 50",
                            "NIFTY 100",
                            "NIFTY 200",
                            "NIFTY 500",
                            "NIFTY MIDCAP 50",
                            "NIFTY MIDCAP 100",
                            "NIFTY MIDCAP 150",
                            "NIFTY BANK",
                            "NIFTY AUTO",
                            "NIFTY MEDIA",] #indics list to get the data

        self.table_head_ls = ["symbol",
                        "identifier",
                        "open",
                        "dayHigh",
                        "dayLow",
                        "lastPrice",
                        "previousClose",
                        "change",
                        "pChange",
                        "totalTradedVolume",
                        "totalTradedValue",
                        "lastUpdateTime",
                        "yearHigh",
                        "yearLow",
                        "perChange365d",
                        "perChange30d"] # List of headings for the table

        # ============== Creating Frame and some default widgets
        self.frame = Frame(self.root).pack()
        title = Label(self.frame, text="Find Favourite Your Stock ", font=(
            "verdana", 16, "bold"), bg="lightblue", borderwidth=7, relief=SUNKEN, height=2)
        title.pack(side=TOP, fill=X)

        # =========== Two Combo Boxes ==============
        self.indics_box = ttk.Combobox(
            self.frame, values=self.list_indics, width=30, font='lucida 16 bold', state='readonly')
        self.indics_box.set("Select The Indics")
        self.indics_box.bind('<<ComboboxSelected>>', self.collect_data)
        self.indics_box.place(x=20, y=100)

        self.company_box = ttk.Combobox(
            self.frame, width=30, font='lucida 16 bold', state='readonly')
        self.company_box.set("Select The Company")
        self.company_box.bind('<<ComboboxSelected>>', self.display_co)

        self.company_box.place(x=530, y=100)

        # =================== Creating Table and Buttons to show the data ================
        self.table_frame = Frame(self.frame)
        self.table_frame.place(x=10,y=200,width=980)

        #=========== style of table and scrool bars ==============
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('Treeview', font='calberia 10 ', rowheight=30)
        style.configure('Treeview.Heading', rowheight=50,
                        font='verdana 12 bold')

        scrlbar_y = Scrollbar(self.table_frame)
        scrlbar_y.pack(fill=Y, side=RIGHT)

        scrlbar_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        scrlbar_x.pack(fill=X, side=BOTTOM)

        self.table = ttk.Treeview(
            self.table_frame,columns=self.table_head_ls, yscrollcommand=scrlbar_y.set, xscrollcommand=scrlbar_x.set)

        scrlbar_y.config(command=self.table.yview)
        scrlbar_x.config(command=self.table.xview)

        #============ setting the columns and the headings =================
        self.table.column("#0", width=0, minwidth=0) # first unwanted coulmn 
        self.table.heading("#0", text="")

        for i in self.table_head_ls:
            self.table.column(i, anchor="center", minwidth=70, width=150)
            self.table.heading(i, text=i)
        
        self.table.pack()

        #================= save as excel btn ===================
        save_btn = Button(self.frame, text="Save Data in Excel", font=(
                "verdana 16 bold"), borderwidth=5, relief=SUNKEN, command=lambda: self.save_exc(), bg="red", fg="white")
        save_btn.place(x=600, y=570, height=50)

    # ==================== From json file or internet collect the data and display in table =================
    def collect_data(self, event):
        try:
            #===== deleting the previous data from table =========
            for item in self.table.get_children():
                self.table.delete(item)

            today = datetime.date.today()
            indic = self.indics_box.get()  # name of selected indic
            path = f"data/{indic} {str(today)}.json"
            self.company_box.set("")

            # ============ if file is not available than downaload the file
            if (os.path.exists(path)==FALSE):
                msgbox.showinfo("Loading","Process is Going On Wait For While.. Press ok ")
                url = "https://latest-stock-price.p.rapidapi.com/price"
                querystring = {"Indices":indic}

                headers = {
                    "X-RapidAPI-Key": "8b95b432c8mshbc8aee1d626616ap199372jsnb71b43f2a8fc",
                    "X-RapidAPI-Host": "latest-stock-price.p.rapidapi.com"
                }

                response = requests.request("GET", url, headers=headers, params=querystring)
                data = json.loads(response.text)
                with open(path,'w') as file:
                    json.dump(data,file)
                msgbox.showinfo('Success',"Process is Done !!")

            # ============== Displaying companies In Company combobox ============
            with open(path, 'r') as file:
                self.data = json.load(file)
            t_list = []
            for i in self.data:
                t_list.append(i['symbol'])

            self.company_box['values'] = t_list
            self.company_box.current(1)

            #=========== Inserting All company data into the table =========
            for i in range(len(self.data)):
                row = self.data[i]
                self.table.insert('', END,values=list(row.values()))
        except Exception as e:
            print(e)
            msgbox.showerror('Error',"Something went wrong!! Check your Internet Connection !!")

    #==================== When select any company this func show the data of that ==============
    def display_co(self,event):
        #===== deleting the previous data from table =========
        company = self.company_box.get()
        for item in self.table.get_children():
            self.table.delete(item)

        #=========== Inserting particular company data into the table =========
        for i in range(len(self.data)):
            row = self.data[i]
            if row['symbol'] == company:
                self.table.insert('', END,values=list(row.values()))   

    #================= Save the data in excel formate ===============================
    def save_exc(self):
        ex_data = {
            "symbol": [],
            "identifier": [],
            "open": [],
            "dayHigh": [],
            "dayLow": [],
            "lastPrice": [],
            "previousClose": [],
            "change": [],
            "pChange": [],
            "totalTradedVolume": [],
            "totalTradedValue": [],
            "lastUpdateTime": [],
            "yearHigh": [],
            "yearLow": [],
            "perChange365d": [],
            "perChange30d": []
        }
        for i in self.data:
            row = i
            for j in ex_data.keys():
                ex_data[j].append(row[j])

        #======== creating dataframe of data to save as excel file ======
        df = pd.DataFrame(ex_data)
        df.to_excel(f'data/{self.indics_box.get()}.xlsx',index=FALSE)

        msgbox.showinfo('File Saved',f"{self.indics_box.get()} Indics Data is Saved in data folder !!")

if __name__ == "__main__":
    root = Tk()
    root.geometry("1000x650")
    root.title("Search things That you Want by 21BCA008 Pratham Rathod")
    root.config(bg="Black")
    root.resizable(0, 0)
    obj = stock(root)
    root.mainloop()