from tkinter import *
from Wiki_main import wiki
from search_main import web
from Stock_main import stock


class main_class():
    def __init__(self,root):
        self.root=root
        # ======= bakc Button to back from any screen =========
        bakc_btn = Button(self.root, text="Back", font=(
            "verdana 16 bold"), command=self.back)
        bakc_btn.place(x=900, y=600)

        # ========= main frame that stores all the widgets =========
        self.main_frame = Frame(self.root, width=1000, height=650, bg="black")
        self.main_frame.pack()

        # ============ All Widgets of main screen ===========
        head = Label(self.main_frame, text="Select Any opetion You Want", font=(
            "verdana", 18, "bold"), bg="lightblue", borderwidth=7, relief=SUNKEN, height=2).place(x=0, y=0, width=1000)
        self.wiki_btn = Button(self.main_frame, text="Search Wiki Pedia", font=(
            "verdana 16 bold"), borderwidth=5, relief=SUNKEN, width=40, command=self.wiki)
        self.wiki_btn.place(x=150, y=200, height=50)

        self.stock_btn = Button(self.main_frame, text="get Share market Details", font=(
            "verdana 16 bold"), borderwidth=5, relief=SUNKEN, width=40, command=self.stock)
        self.stock_btn.place(x=150, y=300, height=50)

        self.search_btn = Button(self.main_frame, text="Search Anything", font=(
            "verdana 16 bold"), borderwidth=5, relief=SUNKEN, width=40, command=self.search)
        self.search_btn.place(x=150, y=400, height=50)

    # ============== bakc button function ==============
    def back(self):
        for child in root.winfo_children():  
            child.destroy()  
        main_class(root)

    # ============== Wikipedia button function ==============
    def wiki(self):
        self.main_frame.destroy()
        wiki(self.root)

    # ============== Stock button function ==============
    def stock(self):
        self.main_frame.destroy()
        stock(self.root)

    # ============== search button function ==============
    def search(self):
        self.main_frame.destroy()
        web(self.root)


if __name__ == "__main__":
     # ========== Creating Default Screen =======
    root = Tk()
    root.geometry("1000x650")
    root.title("Search things That you Want by 21BCA008 Pratham Rathod")
    root.config(bg="Black")
    root.resizable(0, 0)

    obj = main_class(root)
    obj.root.mainloop()