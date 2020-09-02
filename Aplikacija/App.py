from tkinter import *
from tkinter.ttk import *
from pandastable import Table
from Parser import Parser

#window
window = Tk()
window.geometry("1200x800")
window.title("Log parser")

parser = Parser()
parser.SetFilename("test-log.txt")
parser.ReadFile()

window.mainloop()