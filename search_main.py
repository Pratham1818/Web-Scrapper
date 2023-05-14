from tkinter import *
from tkinter import ttk
import requests
import json
import webbrowser
from tkinter import messagebox as msgbox


class web():
    def __init__(self, root):
        # ========== setting the window ==========
        root.title("Find Any Person..")
        self.root = Frame(root,width=1000,height=600,bg="black")
        self.root.pack()
        # ======== creating main window =============

        self.img_btn = Button(self.root, text="Search Image", font=(
            "verdana 14 bold"), borderwidth=5, relief=SUNKEN, command=self.img_search)
        self.img_btn.place(x=10, y=20, width=300)

        self.web_btn = Button(self.root, text="Web Search", font=(
            "verdana 14 bold"), borderwidth=5, relief=SUNKEN, command=self.web_search)
        self.web_btn.place(x=345, y=20, width=300)

        self.news_btn = Button(self.root, text="Search News", font=(
            "verdana 14 bold"), borderwidth=5, relief=SUNKEN, command=self.news_search)
        self.news_btn.place(x=675, y=20, width=300)

        self.frame = Frame(self.root, borderwidth="5",
                           relief="ridge", width=985, height=500, bg="black")
        self.frame.place(x=5, y=100)

    # ========== Developing frame for img download option ============
    def img_search(self):
        # ===== Deleting previous widgets from frame ========
        for widget in self.frame.winfo_children():
            widget.destroy()

        # =============== Inserting Widgets for inputs ===================
        self.img_in = Entry(self.frame, width=30, font=(
            "verdana 12"))  # image title from user
        self.img_in.insert(END, "Enter The Title of Image Here...")
        self.img_in.place(x=10, y=10, height=50)

        self.quan_in = Entry(self.frame, width=30, font=(
            "verdana 12"))  # image Count from user
        self.quan_in.insert(END, "Enter Number of img here...")
        self.quan_in.place(x=350, y=10, height=50)

        self.btn = Button(self.frame, width=15, text="download", font=(
            "verdana 12"), command=self.download_img)
        self.btn.place(x=750, y=10, height=50)

        self.text_area = Text(self.frame, height=15, width=110, font=(
            "Calibri 12 "), bg="black", fg="white")
        self.text_area.place(x=20, y=100)

    # =========== Downloading images from internet ===============
    def download_img(self):
        msgbox.showinfo(
            "Image Download", "Proccess is Going on Wait for while to download the images...")
        img_in = self.img_in.get()
        num = int(self.quan_in.get())

        self.text_area.insert(
            END, f"Downloading {num} images of {img_in}...."+"\n")
        self.text_area.update()

        url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"

        querystring = {"q": img_in, "pageNumber": "1",
                       "pageSize": num, "autoCorrect": "true"}

        headers = {
            "X-RapidAPI-Key": "8b95b432c8mshbc8aee1d626616ap199372jsnb71b43f2a8fc",
            "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
        }
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)

        # ========== downloading image and save in data folder
        try:
            data = data['value']
            for i in range(len(data)):
                result = requests.get(data[i]['url']).content
                with open(f"data/{img_in}{i+1}.jpg", 'wb') as img:
                    img.write(result)
                self.text_area.insert(END, f"{i+1} Image downloaded.."+"\n")
                self.text_area.update()

            msgbox.showinfo(
                "Success", f"{img_in} {num} Images downloaded in data folder !!")
        except Exception as e:
            print(e)
            msgbox.showerror("Error", "Something went Wrong !!")

    def web_search(self):
        # ===== Deleting previous widgets from frame ========
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.search_in = Entry(self.frame, width=60, font=(
            "verdana 12"))  # image Count from user
        self.search_in.insert(END, "Search From here ...")
        self.search_in.place(x=20, y=10, height=50)

        self.btn = Button(self.frame, width=15, text="Search",
                          font=("verdana 12"), command=self.get_weblinks)
        self.btn.place(x=750, y=10, height=50)

        self.text_area = Listbox(self.frame, height=15, width=110, font=(
            "Calibri 12 "), bg="black", fg="white") #Listbox to display the links
        self.text_area.place(x=20, y=100)

    #========= Download the data from internet =============
    def get_weblinks(self):
        try:
            msgbox.showinfo("Searching", "Proccess is Going on Wait for while ...")
            search = self.search_in.get() # Getting the text from search box

            url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI"
            querystring = {"q":search,"pageNumber":"1","pageSize":"10","autoCorrect":"true"}
            headers = {
                "X-RapidAPI-Key": "8b95b432c8mshbc8aee1d626616ap199372jsnb71b43f2a8fc",
                "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            self.data = json.loads(response.text)
            self.data = self.data['value']
        except Exception as e:
            print(e)
            msgbox.showerror("Error","Something Went Wrong !! Check your Internet Connection !!")
        #inserting data in listbox
        for i in self.data:
            self.text_area.insert(END, i['title']+"\n")
            self.text_area.insert(END, i['description']+"\n")
            self.text_area.insert(
                END, "=============================================================================================\n\n")

        #================= Message button and search button ============
        messagebox = Message(self.frame, text="Select The Title And Press Open Web Button below to open the Website..", font=(
            "Verdana", 12, "bold"), bg="black", fg="Red", width=650)
        messagebox.place(x=50, y=420)

        btn = Button(self.frame, width=15, text="Open Browser",
                     font=("verdana 12"), command=self.open_browser)
        btn.place(x=750, y=420, height=50)

    #============== open link on browser function ==========
    def open_browser(self):
        res = self.text_area.get('active') #getting selected text from listbox
        for i in self.data:
            if res == i['title']+"\n" or res == i['description']+"\n":
                webbrowser.open(i['url'])
                break
    
    #============ This Function is for searching the news articals =========
    def news_search(self):
        # ===== Deleting previous widgets from frame ========
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.search_in = Entry(self.frame, width=60, font=(
            "verdana 12"))  # image Count from user
        self.search_in.insert(END, "Search the Topic of news ...")
        self.search_in.place(x=20, y=10, height=50)

        self.btn = Button(self.frame, width=15, text="Search",
                          font=("verdana 12"), command=self.get_newslinks)
        self.btn.place(x=750, y=10, height=50)

        self.text_area = Listbox(self.frame, height=15, width=110, font=(
            "Calibri 12 "), bg="black", fg="white") #Listbox to display the links
        self.text_area.place(x=20, y=100)

    def get_newslinks(self):
        try:
            msgbox.showinfo("Searching", "Proccess is Going on Wait for while ...")
            search = self.search_in.get() # Getting the text from search box

            url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"

            querystring = {"q":search,"pageNumber":"1","pageSize":"10","autoCorrect":"true","fromPublishedDate":"null","toPublishedDate":"null"}

            headers = {
                "X-RapidAPI-Key": "8b95b432c8mshbc8aee1d626616ap199372jsnb71b43f2a8fc",
                "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            self.data = json.loads(response.text)
            self.data = self.data['value']
        except Exception as e:
            print(e)
            msgbox.showerror("Error","Something Went Wrong !! Check your Internet Connection !!")
        #inserting data in listbox
        for i in self.data:
            self.text_area.insert(END, i['title']+"\n")
            self.text_area.insert(END, i['description']+"\n")
            self.text_area.insert(
                END, "=============================================================================================\n\n")

        #================= Message button and search button ============
        messagebox = Message(self.frame, text="Select The Title And Press Open Web Button below to Read The Full Articale ..", font=(
            "Verdana", 12, "bold"), bg="black", fg="Red", width=650)
        messagebox.place(x=50, y=420)

        btn = Button(self.frame, width=15, text="Read Artical",
                     font=("verdana 12"), command=self.open_browser)
        btn.place(x=750, y=420, height=50)

if __name__ == "__main__":
    root = Tk()
    root.geometry("1000x650")
    root.title("Search things That you Want by 21BCA008 Pratham Rathod")
    root.config(bg="Black")
    root.resizable(0, 0)
    web(root)
    root.mainloop()
