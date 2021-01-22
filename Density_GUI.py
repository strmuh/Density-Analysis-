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
        master.iconbitmap(r"C:\Users\Stracey\Documents\Microscopy Density Analysis\venv\cme_logo.ico")
        
        self.style = ttk.Style()
        
        self.style.configure('TFrame', background='#e1d8b9')
        self.style.configure('TButton', background='#e1d8b9')
        self.style.configure('TLabel', background='#e1d8b9', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        self.out_file = StringVar(master)
        self.out_file.set('Results File.xlsx')
        ttk.Label(self.frame_content, text='Output File Name:').grid(row=0, column=0, padx=5, sticky='sw')
        self.out_file_entry = ttk.Entry(self.frame_content, textvariable=self.out_file, width=15, font=('Arial', 10))
        self.out_file_entry.grid(row=1, column=0, pady=2)


        self.images_folder = StringVar(master)
        self.destination_folder = StringVar(master)
        self.str_vars = {'Images Folder':[self.images_folder, self.select_Images_Folder], 'Output File Location':[self.destination_folder,self.select_Output_File_Location]}
        fields2 = 'Images Folder', 'Output File Location'
        for d, td2 in enumerate(fields2, 0):
            self.label = ttk.Entry(self.frame_content, state="disabled", textvariable = self.str_vars[td2][0]).grid(row=1, column=d+1, padx=5, pady=5, sticky='sw')
            ttk.Label(self.frame_content, text=td2).grid(row=0, column=d+1, padx=5, sticky='sw')
            self.str_vars[td2][0].set("C:/")
            ttk.Button(self.frame_content, text='Select Folder', command=self.str_vars[td2][1] ).grid(row=2, column=d+1, padx=5, pady=1,sticky='nsew')
           

        ttk.Button(self.frame_content, text='Submit', command=self.submit).grid(row=25, column=0, padx=5,
                                                                                pady=10, sticky='nsew')
        self.default_threshold = StringVar(master)
        self.default_threshold.set("110")
        self.CheckVar1 = IntVar()
        self.CheckVar2 = IntVar()
        self.man_entry = ttk.Entry(self.frame_content, state="disabled", textvariable = self.default_threshold)
        self.man_entry.grid(row=16, column=1, padx=5, pady=5, sticky='sw')
        self.man_checkbutton = ttk.Checkbutton(self.frame_content, text='Manual Threshold', command = self.manual)
        self.man_checkbutton.state(['!alternate'])
        self.man_checkbutton.grid(row=15, column=1, padx=5,pady=1, sticky='nsew')

        self.saveimage_location = StringVar(master)
        self.saveimage_location.set("C:/")
        self.saveimage_entry = ttk.Entry(self.frame_content, state="disabled", textvariable = self.saveimage_location)
        # self.label2.configure(text = "110")
        self.saveimage_entry.grid(row=1, column=4, padx=5, pady=5, sticky='sw')
        self.saveimage_checkbutton = ttk.Checkbutton(self.frame_content, text='Save Image', command = self.save_images)
        self.saveimage_checkbutton.state(['!alternate'])
        self.saveimage_checkbutton.grid(row=0, column=4, padx=5,pady=1, sticky='nsew')
        self.imgoutbutton = ttk.Button(self.frame_content, text='Select Folder', command=self.images_Output_File_Location, state="disabled")
        self.imgoutbutton.grid(row=2, column=4, padx=5, pady=1, sticky='nsew')

        self.auto_checkbutton = ttk.Checkbutton(self.frame_content, text='Automatic Threshold')
        self.auto_checkbutton.state(['!alternate'])
        self.auto_checkbutton.grid(row=15, column=0, padx=5, pady=1, sticky='nsew')
        self.preview_checkbutton = ttk.Checkbutton(self.frame_content, text='Image Preview')
        self.preview_checkbutton.state(['!alternate'])
        self.preview_checkbutton.grid(row=16, column=0, padx=5, pady=1, sticky='nsew')

    def submit(self):
        self.master.iconbitmap(r"C:\Users\Stracey\Documents\Microscopy Density Analysis\venv\cme_logo.ico")
        a = Determinedensity(self.images_folder.get())
        Outputfiledirectory = 'r"'+self.str_vars['Output File Location'][0].get()+'/'+self.out_file.get()+'"'
        # print(Outputfiledirectory)
        # print(self.saveimage_checkbutton.state())
        # print(self.images_folder.get().split('/')[-1])
        # print(self.saveimage_location.get())
        outfilename = self.out_file.get()
        # print(outfilename)
        if not a.fileList():
            messagebox.showinfo("Error", "No JPG files found in selected folder!")
            return
        if self.preview_checkbutton.state() == ('selected',):
            a.save_images(5, preview=True)
        if self.saveimage_checkbutton.state() == ('selected',):
            print(self.saveimage_location.get())
            a.save_images(self.saveimage_location.get(),save_fig=True)
        if self.man_checkbutton.state() == ('selected',) and self.auto_checkbutton.state() == ('selected',):
            threshold = int(self.man_entry.get())
            a.export_data(man_option=True, auto_option= True,threshold=threshold, filename=outfilename)
            print(a.mandensity(threshold),a.autodensity())
        elif self.man_checkbutton.state() == ('selected',):
            threshold = int(self.man_entry.get())
            a.export_data(man_option=True, threshold=threshold, filename=outfilename)
            print(a.mandensity(threshold))
        elif self.auto_checkbutton.state() == ('selected',):
            a.export_data(auto_option=True, filename=outfilename)
            print(a.autodensity())
        else:
            messagebox.askokcancel("Error", "At least one threshold option must be selected!")
            return
        messagebox.showinfo('Analysis Complete',"Analysis Complete")

        
    def select_Images_Folder (self):
        dirname = filedialog.askdirectory(initialdir="", title="choose your folder")
        self.images_folder.set(dirname)

    def select_Output_File_Location(self):
        dirname = filedialog.askdirectory(initialdir="", title="choose your folder")
        self.destination_folder.set(dirname)
        
    def images_Output_File_Location(self):
        dirname = filedialog.askdirectory(initialdir="", title="choose your folder")
        self.saveimage_location.set(dirname)

    def manual(self):
        if self.man_checkbutton.state()[2] == 'selected':
            self.man_entry.configure(state="")
            # print(self.man_checkbutton.state())
            
        else:
            self.man_entry.configure(state="readonly")
            # print(self.man_checkbutton.state())

    def save_images(self):
        if self.saveimage_checkbutton.state()[2] == 'selected':
            self.saveimage_entry.configure(state="")
            self.imgoutbutton.state(["!disabled"])
            # print(self.man_checkbutton.state())

        else:
            self.saveimage_entry.configure(state="readonly")
            self.imgoutbutton.state(["disabled"])
        


root = Tk()
UI = User_input(root)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
