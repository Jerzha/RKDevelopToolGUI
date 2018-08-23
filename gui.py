import os
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import parameter


class GUI:
    __parameter_parser = None
    __root = None
    __str_loader = None
    __str_parameter = None
    __str_partitions = {}   # {'boot':[True, '<path>', '<status>']}

    __base_row = 0
    __cur_row = 0

    def __init__(self):
        self.__root = Tk()
        self.__root.title("Rockchip DevelopTool GUI")
        self.__str_loader = StringVar(self.__root)
        self.__str_parameter = StringVar(self.__root)
        self.__draw_base_elements()

    def mainloop(self):
        self.__root.mainloop()

    def __draw_base_elements(self):
        Button(self.__root, text='Load From Firmware Folder', command=self.__on_load_firmware_folder).grid(row=self.__cur_row, column=0, padx=5, pady=5, columnspan=1)
        self.__cur_row += 1
        self.__base_row += 1

        Label(self.__root, text='Loader: ').grid(row=self.__cur_row, column=0, padx=10, pady=5)
        Entry(self.__root, textvariable=self.__str_loader, width=50).grid(row=self.__cur_row, column=1, padx=10, pady=5, columnspan=2)
        Button(self.__root, text='...').grid(row=self.__cur_row, column=3, padx=1, pady=5)
        Button(self.__root, text='Upgrade Loader', command=self.__on_upgrade_loader).grid(row=self.__cur_row, column=4, padx=5, pady=5)
        self.__cur_row += 1
        self.__base_row += 1

        Label(self.__root, text='Parameter: ').grid(row=self.__cur_row, column=0, padx=10, pady=5)
        Entry(self.__root, textvariable=self.__str_parameter, width=50).grid(row=self.__cur_row, column=1, padx=10, pady=5, columnspan=2)
        Button(self.__root, text='...', command=self.__on_load_parameter).grid(row=self.__cur_row, column=3, padx=1, pady=5)
        Button(self.__root, text='Write Parameter').grid(row=self.__cur_row, column=4, padx=5, pady=5)
        self.__cur_row += 1
        self.__base_row += 1

        Button(self.__root, text='Select All').grid(row=self.__cur_row, column=0, padx=5, pady=5)

        Button(self.__root, text='Reload Parameter', command=self.__on_reload_parameter).grid(row=self.__cur_row, column=2, padx=5, pady=5)
        Button(self.__root, text='Reset Device').grid(row=self.__cur_row, column=3, padx=5, pady=5)
        Button(self.__root, text='Write LBA').grid(row=self.__cur_row, column=4, padx=5, pady=5)
        self.__cur_row += 1
        self.__base_row += 1

    def __draw_partition_elements(self):
        parts = self.__parameter_parser.partitions
        for kv in parts.keys():
            self.__str_partitions[kv] = [
                BooleanVar(self.__root),    # Checkbox
                StringVar(self.__root),     # Path
                StringVar(self.__root)      # Status
            ]

            Checkbutton(self.__root, text=kv, variable=self.__str_partitions[kv][0], onvalue=True, offvalue=False).grid(row=self.__cur_row, column=0, sticky='W')
            Label(self.__root, text=parts[kv][1]).grid(row=self.__cur_row, column=1)
            Entry(self.__root, textvariable=self.__str_partitions[kv][1], width=35).grid(row=self.__cur_row, column=2, padx=10, pady=5)
            Button(self.__root, text='...', command=self.__load_partition_handler(kv)).grid(row=self.__cur_row, column=3, padx=1, pady=5)
            Label(self.__root, textvariable=self.__str_partitions[kv][2]).grid(row=self.__cur_row, column=4)
            self.__str_partitions[kv][2].set('waiting')
            self.__cur_row += 1

    def __remove_partition_elements(self):
        for i in range(self.__base_row, self.__cur_row):
            widgets = self.__root.grid_slaves(row=i)
            for w in widgets:
                w.grid_forget()

    def __on_load_firmware_folder(self):
        path = tkinter.filedialog.askdirectory()
        if not path:
            return

        if not os.path.exists(path + '/parameter.txt'):
            tkinter.messagebox.showerror(title='Parameter Not Found', message='parameter.txt not found !', icon="warning")
            return
        self.__fill_parameter(path + '/parameter.txt')

        partitions = self.__str_partitions
        for part in partitions.keys():
            img = path + '/' + part + '.img'
            if os.path.exists(img):
                partitions[part][0].set(True)
                partitions[part][1].set(img)


    def __on_upgrade_loader(self):
        pass

    def __on_load_parameter(self):
        a = tkinter.filedialog.askopenfilename()
        self.__fill_parameter(a)

    def __fill_parameter(self, path):
        self.__str_parameter.set(path)
        self.__on_reload_parameter()

    def __on_reload_parameter(self):
        path = self.__str_parameter.get()
        if path:
            self.__parameter_parser = parameter.ParameterParser(path)
            self.__remove_partition_elements()
            self.__cur_row = self.__base_row
            self.__draw_partition_elements()

    def __load_partition_handler(self, key):
        def on_load_partition(k=key):
            a = tkinter.filedialog.askopenfilename()
            self.__str_partitions[k][1].set(a)
            if a != '':
                self.__str_partitions[k][2].set('ready')
        return on_load_partition