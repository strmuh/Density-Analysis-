from Density_calc import Determinedensity
from tkinter import *
from tkinter import ttk

# a = Determinedensity('Centre, As-cast 1')
# a.fileList()
class User_input:
    
    def __init__(self, master):

        self.master = master
        master.title('ARDC Screens')
        master.resizable(True, True)
        master.configure(background='#e1d8b9')
        self.entries_obj = {'SolidsFeedRate_t/h': 45, 'Oversize': 4.6, 'SolidsBulkDensity_t/m3': 1.6}

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#e1d8b9')
        self.style.configure('TButton', background='#e1d8b9')
        self.style.configure('TLabel', background='#e1d8b9', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()
        self.entries = {}

        fields = 'SolidsFeedRate_t/h', 'Oversize', 'SolidsBulkDensity_t/m3'

        for c, td in enumerate(fields, 0):
            ttk.Label(self.frame_content, text=td).grid(row=0, column=c, padx=5, sticky='sw')
            self.td = ttk.Entry(self.frame_content, width=15, font=('Arial', 10))
            self.td.insert(END, self.entries_obj[td])
            self.td.grid(row=1, column=c, padx=5, pady=2)
            self.entries_obj[td] = self.td
            self.entries[td] = self.td.get()

        ttk.Button(self.frame_content, text='Select Folder', command=self.select_folder).grid(row=15, column=0, padx=5, pady=5,sticky='nsew')
        
    def select_folder(self):
        self.dirname = filedialog.askdirectory(initialdir="E:/Images", title="choose your file")
        print(self.dirname)

root = Tk()
UI = User_input(root)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
