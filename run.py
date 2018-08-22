#!/usr/bin/env python3

from tkinter import *
import tkinter.filedialog
import parameter


class GUI:
    __parameter_parser = None
    __root = None
    __str_loader = None
    __str_parameter = None
    __str_partitions = {}

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
        Label(self.__root, text='Loader: ').grid(row=self.__cur_row, column=0, padx=10, pady=5)
        Entry(self.__root, textvariable=self.__str_loader, width=50).grid(row=self.__cur_row, column=1, padx=10, pady=5, columnspan=2)
        Button(self.__root, text='...').grid(row=self.__cur_row, column=3, padx=1, pady=5)
        Button(self.__root, text='Upgrade Loader', command=self.__on_upgrade_loader).grid(row=self.__cur_row, column=4, padx=5, pady=5)
        self.__cur_row += 1

        Label(self.__root, text='Parameter: ').grid(row=self.__cur_row, column=0, padx=10, pady=5)
        Entry(self.__root, textvariable=self.__str_parameter, width=50).grid(row=self.__cur_row, column=1, padx=10, pady=5, columnspan=2)
        Button(self.__root, text='...', command=self.__on_load_parameter).grid(row=self.__cur_row, column=3, padx=1, pady=5)
        Button(self.__root, text='Write Parameter').grid(row=self.__cur_row, column=4, padx=5, pady=5)
        self.__cur_row += 1

        Button(self.__root, text='Select All').grid(row=self.__cur_row, column=0, padx=5, pady=5)
        Button(self.__root, text='Reload Parameter').grid(row=self.__cur_row, column=1, padx=5, pady=5)
        Button(self.__root, text='Write LBA').grid(row=self.__cur_row, column=2, padx=5, pady=5)
        Button(self.__root, text='Reset Device').grid(row=self.__cur_row, column=3, padx=5, pady=5)
        self.__cur_row += 1

    def __draw_partition_elements(self):
        parts = self.__parameter_parser.partitions
        for kv in parts.keys():
            self.__str_partitions[kv] = StringVar(self.__root)
            Checkbutton(self.__root, text=kv).grid(row=self.__cur_row, column=0, sticky='W')
            Label(self.__root, text=parts[kv][1]).grid(row=self.__cur_row, column=1)
            Entry(self.__root, textvariable=self.__str_partitions[kv], width=35).grid(row=self.__cur_row, column=2, padx=10, pady=5)
            Button(self.__root, text='...', command=self.__on_load_parameter).grid(row=self.__cur_row, column=3, padx=1, pady=5)
            self.__cur_row += 1

    def __on_upgrade_loader(self):
        pass

    def __on_load_parameter(self):
        a = tkinter.filedialog.askopenfilename()
        self.__str_parameter.set(a)
        if a != '':
            self.__parameter_parser = parameter.ParameterParser(a)
            self.__draw_partition_elements()


if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()
