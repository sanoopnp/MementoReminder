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

import my_reminder_create_form

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

        self.label_section = Label(self.title_frame, text=text, fg="Orange", bg="Black")
        self.label_section.pack(side="left", fill="x", expand=1)
        self.label_section.bind("<Button>", self.toggle_check_box) 

        self.toggle_button = Checkbutton(self.title_frame, width=2, text='+', command=self.toggle_expand_collapse, variable=self.show, pady=5, borderwidth=2, bg="Black", fg="Orange")
        self.toggle_button.pack(side="left")

        self.sub_frame = Frame(self, relief="sunken", borderwidth=1, bg="Black")

    def toggle_check_box(self, event):
        self.checkbox_toggle()

    def checkbox_toggle(self):
        if bool(self.show.get()):
            self.toggle_button.deselect()
        else:
            self.toggle_button.select()
        self.toggle_expand_collapse()

    def toggle_expand_collapse(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')



class ListReminder(object):
    
    def __init__(self, from_where):
        global root
        root = tk.Tk()
        root.title("List of Reminders")
        root["bg"] = "Black"
        root.lift()
        root.attributes("-topmost", True)
        root.focus_set()
        mainFrame = Frame(root, padx=10, pady = 10, height=10, width=50, bg="Black")
        mainFrame.pack(side=tkinter.LEFT)

        Label(mainFrame, width=42, text='All Entries', fg="Orange", bg="Black").pack(fill="x", expand=1)

        t_frame1 = ToggledFrame(mainFrame, height=10, width=50,text='Active Reminders', relief="raised", borderwidth=1)
        t_frame1.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        t_frame1.label_section.configure(underline=0)
        t_frame2 = ToggledFrame(mainFrame, height=10, width=50,text='Completed Reminders', relief="raised", borderwidth=1)
        t_frame2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        t_frame2.label_section.configure(underline=0)
        t_frame3 = ToggledFrame(mainFrame, height=10, width=50,text='Daily Alarms', relief="raised", borderwidth=1)
        t_frame3.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        t_frame3.label_section.configure(underline=0)
        t_frame5 = ToggledFrame(mainFrame, height=10, width=50,text='Weekly Alarms', relief="raised", borderwidth=1)
        t_frame5.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        t_frame5.label_section.configure(underline=0)
        t_frame4 = ToggledFrame(mainFrame, height=10, width=50,text='Monthly Alarms', relief="raised", borderwidth=1)
        t_frame4.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        t_frame4.label_section.configure(underline=0)

        listbox_active_rem = Listbox(t_frame1.sub_frame, height=10, width=50, fg="Orange", bg="Black")
        listbox_completed_rem = Listbox(t_frame2.sub_frame, height=10, width=50, fg="Orange", bg="Black")
        listbox_daily_alarms = Listbox(t_frame3.sub_frame, height=10, width=50, fg="Orange", bg="Black")
        listbox_monthly_alarms = Listbox(t_frame4.sub_frame, height=10, width=50, fg="Orange", bg="Black")
        listbox_weekly_alarms = Listbox(t_frame5.sub_frame, height=10, width=50, fg="Orange", bg="Black")
        REM_FILE = "reminders.json"
        
        with open(REM_FILE, 'r+') as f:
            entries = json.loads(f.read())
            sl_no = 1

            reminders_json_tree = entries.get('reminders')
            print("reminders_json_tree : ")
            print(json.dumps(reminders_json_tree, indent = 1))
            lines = []
            for item in reminders_json_tree:
                print("item", reminders_json_tree[item])
                lines.append({item:reminders_json_tree[item]})
            print("lines", lines)

            for reminder in entries.get('reminders').items():
                listbox_active_rem.insert(END, str(sl_no) + ". " + str(reminder[1].get('reminder') + ' (on ' + str(reminder[1].get('date')) + ')    \t[' + str(reminder[0]) +']'))
                sl_no += 1
            sl_no = 1
            for reminder in entries.get('completed_reminders').items():
                listbox_completed_rem.insert(END, str(sl_no) + ". " + str(reminder[1].get('reminder') + '    \t[' + str(reminder[0]) +']'))
                sl_no += 1
            sl_no = 1
            for reminder in entries.get('daily_alarms').items():
                listbox_daily_alarms.insert(END, str(sl_no) + ". " + str(reminder[1].get('reminder') + ' (@ ' + str(reminder[1].get('time')) + ')    \t[' + str(reminder[0]) +']'))
                sl_no += 1
            sl_no = 1
            for reminder in entries.get('weekly_alarms').items():
                listbox_weekly_alarms.insert(END, str(sl_no) + ". " + str(reminder[1].get('reminder') + ' (on days ' + str(reminder[1].get('day_of_week')) + ')    \t[' + str(reminder[0]) +']'))
                sl_no += 1
            sl_no = 1
            for reminder in entries.get('monthly_alarms').items():
                listbox_monthly_alarms.insert(END, str(sl_no) + ". " + str(reminder[1].get('reminder') + ' (on day ' + str(reminder[1].get('day_of_month')) + ')    \t[' + str(reminder[0]) +']'))
                sl_no += 1
        listbox_active_rem.pack(ipadx=10, ipady=10, )
        listbox_completed_rem.pack()
        listbox_daily_alarms.pack()
        listbox_monthly_alarms.pack()
        listbox_weekly_alarms.pack()

        listbox_active_rem.bind("<<ListboxSelect>>", self.list_selection_change_callback)
        listbox_completed_rem.bind("<<ListboxSelect>>", self.list_selection_change_callback)
        listbox_daily_alarms.bind("<<ListboxSelect>>", self.list_selection_change_callback)
        listbox_monthly_alarms.bind("<<ListboxSelect>>", self.list_selection_change_callback)
        listbox_weekly_alarms.bind("<<ListboxSelect>>", self.list_selection_change_callback)

        buttonFrame = Frame(mainFrame, padx=10, pady=10, bg="Black")
        btn1 = Button(buttonFrame, text="Close.", underline=5, command=self.close, fg="Orange", bg="Black").grid(row=0, column=0)
        btn2 = Button(buttonFrame, text="Back", underline=0, command=self.openCreateReminder, fg="Orange", bg="Black").grid(row=0, column=1)
        buttonFrame.grid_columnconfigure(1, minsize=10)
        buttonFrame.pack()

        root.bind('<Alt-.>', lambda event: self.close())
        root.bind('<Alt-a>', lambda event: self.expand_targeted_and_collapse_all_others(t_frame1, [t_frame2, t_frame3, t_frame4, t_frame5]))
        root.bind('<Alt-c>', lambda event: self.expand_targeted_and_collapse_all_others(t_frame2, [t_frame1, t_frame3, t_frame4, t_frame5]))
        root.bind('<Alt-d>', lambda event: self.expand_targeted_and_collapse_all_others(t_frame3, [t_frame1, t_frame2, t_frame4, t_frame5]))
        root.bind('<Alt-m>', lambda event: self.expand_targeted_and_collapse_all_others(t_frame4, [t_frame1, t_frame2, t_frame3, t_frame5]))
        root.bind('<Alt-w>', lambda event: self.expand_targeted_and_collapse_all_others(t_frame5, [t_frame1, t_frame2, t_frame3, t_frame4]))
        root.bind('<Alt-b>', lambda event: self.openCreateReminder())

        if from_where == 'from_reminder_create_from': #to bring the the window on top of others
            root.iconify()
            root.update()
            root.deiconify()

        root.mainloop()

    def expand_targeted_and_collapse_all_others(self, target_frame, other_frames):
        target_frame.checkbox_toggle()
        for each_frame in other_frames:
            each_frame.toggle_button.deselect()
            each_frame.toggle_expand_collapse()

    def list_selection_change_callback(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            print('item selected : ' + str(index) + ' : ' + str(data))
        
        import re
        rem_id = re.search('(.*)(\[)(.*)(\])', str(data)).group(3)

        with open(REM_FILE, 'r+') as f:
            reminders = json.loads(f.read())
            type_of_entry = 'active_reminder'
            if reminders.get('reminders').get(rem_id):
                x = reminders.get('reminders').get(rem_id)
                print('item from active list : ' + str(x))
            elif reminders.get('completed_reminders').get(rem_id):
                x = reminders.get('completed_reminders').get(rem_id)
                print('item from completed list : ' + str(x))
                type_of_entry = 'completed_reminder'
            elif reminders.get('daily_alarms').get(rem_id):
                x = reminders.get('daily_alarms').get(rem_id)
                print('item from daily alarms list : ' + str(x))
                type_of_entry = 'daily_alarm'
            elif reminders.get('monthly_alarms').get(rem_id):
                x = reminders.get('monthly_alarms').get(rem_id)
                print('item from monthly alarms list : ' + str(x))
                type_of_entry = 'monthly_alarm'
            elif reminders.get('weekly_alarms').get(rem_id):
                x = reminders.get('weekly_alarms').get(rem_id)
                print('item from weekly alarms list : ' + str(x))
                type_of_entry = 'weekly_alarm'
            global rem_obj
            rem_obj = (rem_id,x)
            self.openEditReminder(type_of_entry)

    def openEditReminder(self, type_of_entry):
        print('rem obj : ' + str(rem_obj))
        global root
        root.destroy()
        my_reminder_create_form.Reminder(rem_obj, type_of_entry)

    def openCreateReminder(self):
        global root
        root.destroy()
        my_reminder_create_form.Reminder()

    def close(self):
        '''
        utility function to close window
        '''
        root.destroy()



if __name__ == "__main__":
	ListReminder('main')
