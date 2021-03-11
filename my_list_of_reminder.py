try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
import json
import sys
import os
import tkinter
import tkinter.ttk
import datetime
import tkinter as tk
from tkinter import ttk 

REM_FILE = "reminders.json"

rem_obj = {}
root = None

class ToggledFrame(tkinter.Frame):

    def __init__(self, parent, text="", *args, **options):
        Frame.__init__(self, parent, *args, **options)

        self.show = IntVar()
        self.show.set(0)

        self.title_frame = Frame(self, bg="Black")
        self.title_frame.pack(fill="x", expand=1)

        Label(self.title_frame, text=text, fg="Orange", bg="Black").pack(side="left", fill="x", expand=1)

        self.toggle_button = Checkbutton(self.title_frame, width=2, text='+', command=self.toggle, variable=self.show, bg="Black", fg="Orange")
        self.toggle_button.pack(side="left")

        self.sub_frame = Frame(self, relief="sunken", borderwidth=1, bg="Black")


    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')

class ListReminder(object):
    
    def __init__(self):
        global root
        root = tk.Tk()
        root.title("Set reminder")
        root["bg"] = "Black"
        mainFrame = Frame(root, padx=10, pady = 10, height=10, width=50, bg="Black")
        mainFrame.pack(side=tkinter.LEFT)

        Label(mainFrame, width=42, text='All Entries', fg="Orange", bg="Black").pack(fill="x", expand=1)

        t_frame = ToggledFrame(mainFrame, height=10, width=50,text='Active Reminders', relief="raised", borderwidth=1)
        t_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        t_frame2 = ToggledFrame(mainFrame, height=10, width=50,text='Completed Reminders', relief="raised", borderwidth=1)
        t_frame2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")


        listbox_active_rem = Listbox(t_frame.sub_frame, height=10, width=50, fg="Orange", bg="Black")
        listbox_completed_rem = Listbox(t_frame2.sub_frame, height=10, width=50, fg="Orange", bg="Black")
        REM_FILE = "reminders.json"
        with open(REM_FILE, 'r+') as f:
            entries = json.loads(f.read())
            for reminder in entries.get('reminders').items():
                listbox_active_rem.insert(END, str(reminder[1].get('reminder') + '    \t[' + str(reminder[0]) +']'))
            for reminder in entries.get('completed_reminders').items():
                listbox_completed_rem.insert(END, str(reminder[1].get('reminder') + '    \t[' + str(reminder[0]) +']'))
        listbox_active_rem.pack()
        listbox_completed_rem.pack()
        listbox_active_rem.bind("<<ListboxSelect>>", self.list_selection_change_callback)
        listbox_completed_rem.bind("<<ListboxSelect>>", self.list_selection_change_callback)

        buttonFrame = Frame(mainFrame, padx=10, pady=10, bg="Black")
        btn1 = Button(buttonFrame, text="Close", command=self.close, fg="Orange", bg="Black").grid(row=0, column=0)
        buttonFrame.grid_columnconfigure(1, minsize=10)
        buttonFrame.pack()

        root.mainloop()
    
    def list_selection_change_callback(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            # Reminder(self.reminder)
        print('data : ' + str(index) + ' : ' + str(data))
        
        import re
        rem_id = re.search('(.*)(\[)(.*)(\])', str(data)).group(3)
        print(rem_id)

        with open(REM_FILE, 'r+') as f:
            reminders = json.loads(f.read())
            x = reminders.get('reminders').get(rem_id)
            if x:
                print('item from active list : ' + str(x))
            else:
                x = reminders.get('completed_reminders').get(rem_id)
                print('item from completed list : ' + str(x))
            global rem_obj
            rem_obj = (rem_id,x)
            print('rem obj : ' + str(rem_obj))
            self.openEditReminder()

    def openEditReminder(self):
        print('rem obj : ' + str(rem_obj))
        global root
        root.destroy()
        import my_reminder_create_form
        my_reminder_create_form.Reminder(rem_obj)

    def close(self):
        '''
        utility function to close window
        '''
        import os
        sys.exit()


if __name__ == "__main__":
	ListReminder()