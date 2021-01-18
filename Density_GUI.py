from Density_calc import Determinedensity
from tkinter import *
from tkinter import ttk

# a = Determinedensity('Centre, As-cast 1')
# a.fileList()
class User_input:
    
    def __init__(self, master):

        self.master = master
        master.title('Microscopy Analysis Program')
        master.resizable(True, True)
        master.configure(background='#e1d8b9')
        self.entries_obj = {'Output File Name': 'Test Result.xlsx', 'Oversize': 4.6, 'SolidsBulkDensity_t/m3': 1.6}
        self.style = ttk.Style()
        
        self.style.configure('TFrame', background='#e1d8b9')
        self.style.configure('TButton', background='#e1d8b9')
        self.style.configure('TLabel', background='#e1d8b9', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()
        self.entries = {}

        fields = 'Output File Name', 'Oversize', 'SolidsBulkDensity_t/m3'

        for c, td in enumerate(fields, 0):
            ttk.Label(self.frame_content, text=td).grid(row=0, column=c, padx=5, sticky='sw')
            self.td = ttk.Entry(self.frame_content, width=15, font=('Arial', 10))
            self.td.insert(END, self.entries_obj[td])
            self.td.grid(row=1, column=c, padx=5, pady=2)
            self.entries_obj[td] = self.td
            self.entries[td] = self.td.get()
        
        self.text = StringVar(master)
        self.label = ttk.Entry(self.frame_content, state="disabled", textvariable = self.text).grid(row=1, column=3, padx=5, pady=5, sticky='sw')
        ttk.Label(self.frame_content, text='Images Folder').grid(row=0, column=3, padx=5, sticky='sw')
        self.text.set("C:/")
        ttk.Button(self.frame_content, text='Select Folder', command=self.select_folder).grid(row=15, column=3, padx=5, pady=1,sticky='nsew')
        ttk.Button(self.frame_content, text='Submit', command=self.submit).grid(row=20, column=0, padx=5,
                                                                                              pady=1, sticky='nsew')
        self.default_threshold = StringVar(master)
        self.default_threshold.set("110")
        self.CheckVar1 = IntVar()
        self.CheckVar2 = IntVar()
        # self.CheckVar1.set(1)
        # self.CheckVar2.set(1)
        self.man_entry = ttk.Entry(self.frame_content, state="disabled", textvariable = self.default_threshold)
        # self.label2.configure(text = "110")
        self.man_entry.grid(row=15, column=2, padx=5, pady=5, sticky='sw')
        self.man_checkbutton = ttk.Checkbutton(self.frame_content, text='Manual Threshold', command = self.manual)
        self.man_checkbutton.state(['!alternate'])
        self.man_checkbutton.grid(row=15, column=1, padx=5,pady=1, sticky='nsew')
        self.auto_checkbutton = ttk.Checkbutton(self.frame_content, text='Automatic Threshold')
        self.auto_checkbutton.state(['!alternate'])
        self.auto_checkbutton.grid(row=15, column=0, padx=5, pady=1, sticky='nsew')
        self.preview_checkbutton = ttk.Checkbutton(self.frame_content, text='Image Preview')
        self.preview_checkbutton.state(['!alternate'])
        self.preview_checkbutton.grid(row=16, column=0, padx=5, pady=1, sticky='nsew')

    def submit(self):
        a = Determinedensity(self.text.get())
        print(a.fileList())
        if not a.fileList():
            messagebox.askokcancel("Error", "No JPG files found in selected folder!")
            return 
        if self.man_checkbutton.state() == ('selected',) and self.auto_checkbutton.state() == ('selected',):
            threshold = int(self.man_entry.get())
            a.export_data(man_option=True, auto_option= True,threshold=threshold)
            print(a.mandensity(threshold),a.autodensity())
        elif self.man_checkbutton.state() == ('selected',):
            threshold = int(self.man_entry.get())
            a.export_data(man_option=True, threshold=threshold)
            print(a.mandensity(threshold))
        elif self.auto_checkbutton.state() == ('selected',):
            a.export_data(auto_option=True, threshold=threshold)
            print(a.autodensity())
        elif self.preview_checkbutton.state() == ('selected',):
            a.save_images(5, preview=True)
        else:
            messagebox.askokcancel("Error", "At least one threshold option must be selected!")
            return 

        # print(a.fileList())
        
        
    def select_folder(self):
        dirname = filedialog.askdirectory(initialdir="", title="choose your file")
        self.text.set(dirname)

    def manual(self):
        if self.man_checkbutton.state()[2] == 'selected':
            self.man_entry.configure(state="")
            # print(self.man_checkbutton.state())
            
        else:
            self.man_entry.configure(state="readonly")
            # print(self.man_checkbutton.state())
            # 
        


root = Tk()
root.wm_iconbitmap(r"C:\Users\Stracey\Documents\Microscopy Density Analysis\venv\uct_logo.ico")
UI = User_input(root)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
