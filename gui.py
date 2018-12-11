import os
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
    import tkFileDialog as tkFileDialog
    import tkMessageBox as tkMessageBox
    from Tkinter import *
    import thread
elif sys.version_info.major == 3:
    import tkinter as tk
    import tkinter.filedialog as tkFileDialog
    import tkinter.messagebox as tkMessageBox
    from tkinter import *
    import _thread as thread
import parameter
import cmd
import re


class GUI:
    __parameter_parser = None
    __root = None
    __str_loader = None
    __str_parameter = None
    __str_partitions = {}   # {'boot':[True, '<path>', '<status>']}
    __is_select_all = None
    __str_usb_status = None

    __base_row = 0
    __cur_row = 0

    def __init__(self):
        ret, ver = cmd.version()
        if ret != 0:
            tk.messagebox.showerror(title='Error', message='rkdeveloptool running error!\n' + ver)
            exit(0)

        self.__root = tk.Tk()
        self.__root.title("Rockchip DevelopTool GUI  (" + ver + ")")
        self.__str_loader = tk.StringVar(self.__root)
        self.__str_parameter = tk.StringVar(self.__root)
        self.__is_select_all = tk.BooleanVar(self.__root)
        self.__str_usb_status = tk.StringVar(self.__root)
        self.__draw_base_elements()

        thread.start_new_thread(self.__thread_check_usb, ())

    def mainloop(self):
        self.__root.mainloop()

    def load_image_path(self, path):
        if path is None or path == '':
            return

        self.__fill_parameter(path + '/parameter.txt')
        if os.path.exists(path + '/MiniLoaderAll.bin'):
            self.__str_loader.set(path + '/MiniLoaderAll.bin')

        partitions = self.__str_partitions
        for part in partitions.keys():
            img = path + '/' + part + '.img'
            if os.path.exists(img):
                partitions[part][0].set(True)
                partitions[part][1].set(img)
                partitions[part][2].set('Ready')

    def __thread_check_usb(self):
        while True:
            ret, res = cmd.list_device()
            self.__str_usb_status.set(res)
            time.sleep(1)

    def __draw_base_elements(self):
        Button(self.__root, text='Load Firmwares From Folder', command=self.__on_load_firmware_folder).grid(row=self.__cur_row, column=0, padx=5, pady=5, columnspan=2, sticky='W')
        Label(self.__root, textvariable=self.__str_usb_status).grid(row=self.__cur_row, column=2, padx=5, pady=5, columnspan=3, sticky='E')
        self.__cur_row += 1
        self.__base_row += 1

        Label(self.__root, text='Loader: ').grid(row=self.__cur_row, column=0, padx=10, pady=5, sticky='W')
        Entry(self.__root, textvariable=self.__str_loader, width=50).grid(row=self.__cur_row, column=1, padx=10, pady=5, columnspan=2)
        Button(self.__root, text='...', command=self.__on_load_loader).grid(row=self.__cur_row, column=3, padx=1, pady=5)
        Button(self.__root, text='Upgrade Loader', command=self.__on_upgrade_loader).grid(row=self.__cur_row, column=4, padx=5, pady=5)
        self.__cur_row += 1
        self.__base_row += 1

        Label(self.__root, text='Parameter: ').grid(row=self.__cur_row, column=0, padx=10, pady=5, sticky='W')
        Entry(self.__root, textvariable=self.__str_parameter, width=50).grid(row=self.__cur_row, column=1, padx=10, pady=5, columnspan=2)
        Button(self.__root, text='...', command=self.__on_load_parameter).grid(row=self.__cur_row, column=3, padx=1, pady=5)
        Button(self.__root, text='Write Parameter', command=self.__on_writing_parameter).grid(row=self.__cur_row, column=4, padx=5, pady=5)
        self.__cur_row += 1
        self.__base_row += 1

        Checkbutton(self.__root, text='Select All', variable=self.__is_select_all, command=self.__on_select_all).grid(row=self.__cur_row, column=0, sticky='W', padx=10, pady=5)
        pk = Frame(self.__root)
        pk.grid(row=self.__cur_row, column=1, padx=5, pady=5, columnspan=4, sticky='E')
        Button(pk, text='Reload Parameter', command=self.__on_reload_parameter).grid(row=self.__cur_row, column=1, padx=5, pady=5)
        Button(pk, text='Reset Device', command=self.__on_reset_device).grid(row=self.__cur_row, column=2, padx=5, pady=5)
        Button(pk, text='Write Selected LBAs', command=self.__on_write_selected_lbas).grid(row=self.__cur_row, column=3, padx=5, pady=5)
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

            Checkbutton(self.__root, text=kv, variable=self.__str_partitions[kv][0]).grid(row=self.__cur_row, column=0, sticky='W', padx=10, pady=5)
            Label(self.__root, text=parts[kv][1]).grid(row=self.__cur_row, column=1)
            Entry(self.__root, textvariable=self.__str_partitions[kv][1], width=35).grid(row=self.__cur_row, column=2, padx=10, pady=5)
            Button(self.__root, text='...', command=self.__load_partition_handler(kv)).grid(row=self.__cur_row, column=3, padx=1, pady=5)
            Label(self.__root, textvariable=self.__str_partitions[kv][2]).grid(row=self.__cur_row, column=4)
            self.__str_partitions[kv][2].set('No File')
            self.__cur_row += 1

    def __remove_partition_elements(self):
        for i in range(self.__base_row, self.__cur_row):
            widgets = self.__root.grid_slaves(row=i)
            for w in widgets:
                w.grid_forget()

    def __on_reset_device(self):
        ret, str = cmd.reset_device()

    def __on_load_firmware_folder(self):
        path = tkFileDialog.askdirectory()
        if not path:
            return

        if not os.path.exists(path + '/parameter.txt'):
            tkMessageBox.showwarning(title='Parameter Not Found', message='parameter.txt not found !')
            return

        self.load_image_path(path)

    def __on_load_loader(self):
        path = tkFileDialog.askopenfilename()
        if path != '':
            self.__str_loader.set(path)

    def __on_upgrade_loader(self):
        ret, res = cmd.upgrade_loader(self.__str_loader.get())
        if ret == 0:
            tkMessageBox.showinfo("Success", "Upgrade loader success.")
        else:
            tkMessageBox.showerror("Failure", "Upgrade loader failure.")

    def __on_writing_parameter(self):
        ret, res = cmd.write_parameter(self.__str_parameter.get())
        if ret == 0:
            tkMessageBox.showinfo("Success", "Writing parameter success.")
        else:
            tkMessageBox.showerror("Failure", "Writing parameter failure.")

    def __on_load_parameter(self):
        a = tkFileDialog.askopenfilename()
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
            a = tkFileDialog.askopenfilename()
            self.__str_partitions[k][1].set(a)
            if a != '':
                self.__str_partitions[k][2].set('ready')
        return on_load_partition

    def __on_select_all(self):
        print(self.__is_select_all.get())
        parts = self.__str_partitions
        if self.__is_select_all.get():
            for val in parts.keys():
                parts[val][0].set(True)
        else:
            for val in parts.keys():
                parts[val][0].set(False)

    def __on_write_selected_lbas(self):
        parts = self.__str_partitions
        for k in parts.keys():
            if parts[k][0].get():
                parts[k][2].set('Waiting')
        thread.start_new_thread(self.__thread_write_selected_lbas, ())

    def __thread_write_selected_lbas(self):
        parts = self.__str_partitions
        partitions = self.__parameter_parser.partitions

        for k in parts.keys():
            if parts[k][0].get():
                parts[k][2].set('Writing ...')
                p = cmd.write_lba_bysec_async(partitions[k][1], parts[k][1].get())

                while p.poll() is None:
                    line = p.stdout.readline()
                    obj = re.search('\((\d+)%\)', str(line))
                    parts[k][2].set("Writing " + obj.group(0))

                if p.returncode == 0:
                    parts[k][2].set('Success')
                else:
                    parts[k][2].set('Failed')
                    tkMessageBox.showerror(title='Failed', message='writing lba error!\n')
                    return
