from tkinter import Tk, ttk, Button, Label, Entry, messagebox, Checkbutton, Frame, LabelFrame, Scrollbar, END, IntVar
from Parser import Parser
from datetime import date

def loadFile():
    #filename = filenameInput.get()
    filename = "access-log.txt"
    filenameInput.delete(0, END)
    if len(filename) > 0:
        try:
            parser.ClearData()
            parser.SetFilename(filename)
            messagebox.showinfo("Uspjeh!", "Datoteka učitana!")
            loadedFileLabel.config(text = filename, foreground="red")
            fillDataTable()
        except:
            messagebox.showwarning("Greška", "Datoteka nije pronađena!")
    else:
        messagebox.showwarning("Greška", "Unesite naziv datoteke!")

def clearTable():
    dataTable.delete(*dataTable.get_children())

def fillDataTable():
    clearTable()
    dataTable["column"] = list(parser.DataFrame.columns)
    dataTable["show"] = "headings"
    for column in dataTable["columns"]:
        dataTable.heading(column, text=column)

    dataFrameRows = parser.DataFrame.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in dataFrameRows:
        dataTable.insert("", "end", values=row)

#------------------------------------------------parser------------------------------------------------
parser = Parser()

#------------------------------------------------window------------------------------------------------
window = Tk()
window.geometry("1200x800")
window.resizable(0, 0)
window.title("Log parser")
#window.pack_propagate(False)

#----------------------------------------------fileselect----------------------------------------------
filenameLabel = Label(window, text="Naziv datoteke:")
filenameLabel.place(x=10, y=0)

loadedFileLabel = Label(window, text="")
loadedFileLabel.place(x=95, y=0)

filenameInput = Entry(window, width=20, highlightcolor="red", highlightthickness=1)
filenameInput.place(x=10, y=25)

filenameButton = Button(window, text="Učitaj datoteku", command=loadFile)
filenameButton.place(x=10, y=50)

#----------------------------------------------checkboxes----------------------------------------------
varClientIP = IntVar()
varClientID = IntVar()
varUsername = IntVar()
varDate = IntVar()
varContent = IntVar()
varHTTP = IntVar()
varBytes = IntVar()
varRef = IntVar()
varAgent = IntVar()

checkboxesFrame = Frame(window, height=120, width=600, borderwidth=2, relief="groove")
checkboxesFrame.place(x=200, y=0)

refreshButton = Button(window, text="Osvježi prikaz")
refreshButton.place(x=310, y=85)

clientIPCheckbox = Checkbutton(checkboxesFrame, text="IP klijenta", variable=varClientIP)
clientIPCheckbox.grid(row=0, column=0)
clientIPCheckbox.select()

clientIDCheckbox = Checkbutton(checkboxesFrame, text="ID korisnika", variable=varClientID)
clientIDCheckbox.grid(row=1, column=0)
clientIDCheckbox.select()

usernameCheckbox = Checkbutton(checkboxesFrame, text="Korisničko ime", variable=varUsername)
usernameCheckbox.grid(row=2, column=0)
usernameCheckbox.select()

dateCheckbox = Checkbutton(checkboxesFrame, text="Datum", variable=varDate)
dateCheckbox.grid(row=0, column=1)
dateCheckbox.select()

contentCheckbox = Checkbutton(checkboxesFrame, text="Sadržaj", variable=varContent)
contentCheckbox.grid(row=1, column=1)
contentCheckbox.select()

httpCheckbox = Checkbutton(checkboxesFrame, text="HTTP status", variable=varHTTP)
httpCheckbox.grid(row=2, column=1)
httpCheckbox.select()

bytesCheckbox = Checkbutton(checkboxesFrame, text="Količina bajtova", variable=varBytes)
bytesCheckbox.grid(row=0, column=2)
bytesCheckbox.select()

refCheckbox = Checkbutton(checkboxesFrame, text="Refereer", variable=varRef)
refCheckbox.grid(row=1, column=2)
refCheckbox.select()

agentCheckbox = Checkbutton(checkboxesFrame, text="Agent", variable=varAgent)
agentCheckbox.grid(row=2, column=2)
agentCheckbox.select()

#------------------------------------------------search------------------------------------------------
searchLabel = Label(window, text="Pretraga:")
searchLabel.place(x=10, y=330)

searchInput = Entry(window, width=20, highlightcolor="red", highlightthickness=1)
searchInput.place(x=65, y=330)

searchButton = Button(window, text="Pretraži")
searchButton.place(x=200, y=327)

#-----------------------------------------------datatable----------------------------------------------
dataFrame = LabelFrame(window, text="Sadržaj datoteke:")
dataFrame.place(height=400, width=1200, x=0, y=360)

dataTable = ttk.Treeview(dataFrame)
dataTable.place(relheight=1, relwidth=1)

dataTableBarX = Scrollbar(dataFrame, orient="horizontal", command=dataTable.xview)
dataTableBarY = Scrollbar(dataFrame, orient="vertical", command=dataTable.yview)
dataTable.configure(xscrollcommand=dataTableBarX.set, yscrollcommand=dataTableBarY.set)
dataTableBarX.pack(side="bottom", fill="x")
dataTableBarY.pack(side="right", fill="y")

#-------------------------------------------------quit-------------------------------------------------
quitButton = Button(window, text="Izlaz", width=10, command=window.quit)
quitButton.place(x=1110, y=770)

window.mainloop()