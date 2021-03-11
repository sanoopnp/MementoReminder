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

REM_FILE = "reminders.json"

class AutocompleteCombobox(tkinter.ttk.Combobox):

	def set_completion_list(self, completion_list):
			"""Use our completion list as our drop down selection menu, arrows move through menu."""
			self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
			self._hits = []
			self._hit_index = 0
			self.position = 0
			self.fg = "Orange"
			self.bg = 'Black'
			self.bind('<KeyRelease>', self.handle_keyrelease)
			self['values'] = self._completion_list  # Setup our popup menu

	def autocomplete(self, delta=0):
			"""autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
			if delta: # need to delete selection otherwise we would fix the current position
					self.delete(self.position, tkinter.END)
			else: # set position to end so selection starts where textentry ended
					self.position = len(self.get())
			# collect hits
			_hits = []
			for element in self._completion_list:
					if element.lower().startswith(self.get().lower()): # Match case insensitively
							_hits.append(element)
			# if we have a new hit list, keep this in mind
			if _hits != self._hits:
					self._hit_index = 0
					self._hits=_hits
			# only allow cycling if we are in a known hit list
			if _hits == self._hits and self._hits:
					self._hit_index = (self._hit_index + delta) % len(self._hits)
			# now finally perform the auto completion
			if self._hits:
					self.delete(0,tkinter.END)
					self.insert(0,self._hits[self._hit_index])
					self.select_range(self.position,tkinter.END)

	def handle_keyrelease(self, event):
			"""event handler for the keyrelease event on this widget"""
			if event.keysym == "BackSpace":
					self.delete(self.index(tkinter.INSERT), tkinter.END)
					self.position = self.index(tkinter.END)
			if event.keysym == "Left":
					if self.position < self.index(tkinter.END): # delete the selection
							self.delete(self.position, tkinter.END)
					else:
							self.position = self.position-1 # delete one character
							self.delete(self.position, tkinter.END)
			if event.keysym == "Right":
					self.position = self.index(tkinter.END) # go to end (no selection)
			if len(event.keysym) == 1:
					self.autocomplete()
			# No need for up/down, we'll jump to the popup
			# list at the position of the autocompletion



# class ToggledFrame(tkinter.Frame):

#     def __init__(self, parent, text="", *args, **options):
#         Frame.__init__(self, parent, *args, **options)

#         self.show = IntVar()
#         self.show.set(0)

#         self.title_frame = Frame(self, bg="Black")
#         self.title_frame.pack(fill="x", expand=1)

#         Label(self.title_frame, text=text, fg="Orange", bg="Black").pack(side="left", fill="x", expand=1)

#         self.toggle_button = Checkbutton(self.title_frame, width=2, text='+', command=self.toggle, variable=self.show, bg="Black", fg="Orange")
#         self.toggle_button.pack(side="left")

#         self.sub_frame = Frame(self, relief="sunken", borderwidth=1, bg="Black")


#     def toggle(self):
#         if bool(self.show.get()):
#             self.sub_frame.pack(fill="x", expand=1)
#             self.toggle_button.configure(text='-')
#         else:
#             self.sub_frame.forget()
#             self.toggle_button.configure(text='+')



class Reminder(object):

	def __init__(self, rem_tuple=None):

		self.root = Tk()
		self.root.title("Set reminder")
		self.root["bg"] = "Black"
		from tkinter import ttk
		combostyle = ttk.Style()
		combostyle.theme_create('combostyle', parent='alt',
			settings = {'TCombobox':
						{'configure':
						{'fieldbackground': 'Black', 'background': 'Orange', 'foreground' : 'Cyan',}
						}}
			)
		combostyle.theme_use('combostyle') 
		self.position_window()
		
		now = datetime.datetime.now()
		month_list = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
		self.reminder_as_param = rem_tuple
		print('reminder_as_param : ' + str(self.reminder_as_param))
		print('current date_time : ' + str(now.year) + " : " + str(now.month) + " : " + str(now.day) + " : " + str(now.hour) + " : " + str(now.minute))
		
		self.recursive_value = IntVar()
		self.day_value= IntVar()
		self.month_value = StringVar()
		self.year_value = IntVar()
		self.hrs_value = IntVar()
		self.mins_value = IntVar()
		self.am_pm_value = StringVar()

		if self.reminder_as_param:
			self.rem_value.set(self.reminder_as_param[1].get('reminder'))
			self.recursive_value.set(0)
			date_parts = self.reminder_as_param[1].get('date').split('-')
			time_parts = self.reminder_as_param[1].get('time').split(':')
			self.day_value.set(str(date_parts[0]).zfill(2))
			self.month_value.set(str(date_parts[1]).zfill(2))
			self.year_value.set(str(date_parts[2]).zfill(2))
			self.hrs_value.set(str(time_parts[0]).zfill(2))
			self.mins_value.set(str(time_parts[1]).zfill(2))
			self.am_pm_value.set(str(time_parts[2]).zfill(2))
		else:
			self.recursive_value.set(0)
			self.day_value.set(str(now.day).zfill(2))
			self.month_value.set(month_list[now.month-1])
			self.year_value.set(now.year)
			self.hrs_value.set(str(now.hour%12).zfill(2))
			time_min = now.minute+1 if (now.minute+1) < 59 else 59
			self.mins_value.set(str(time_min).zfill(2))
			if now.hour >= 12:
				self.am_pm_value.set('PM')
			else:
				self.am_pm_value.set('AM')
		
		# main frame (inside root) config
		self.mainFrame = Frame(self.root, padx=10, pady = 10, bg="Black")
		self.mainFrame.pack(side=tkinter.LEFT)

		# first field frame (inside main frame) config
		self.fieldRow1 = Frame(self.mainFrame, padx=5, pady=5, bg="Black")
		Label(self.fieldRow1, text="Remind me \n about:", fg="Orange", bg="Black").grid(row=0, column=0)
		self.rem = Text(self.fieldRow1, height=3, width=20, fg="Cyan", bg="Black")
		if self.reminder_as_param:
			self.rem.insert(END, self.reminder_as_param[1].get('reminder'))
		self.rem.grid(row=0, column=1)
		self.rem.focus_set() 
		self.rem.focus()

		self.recursive = Checkbutton(self.fieldRow1, text='Recursive', fg="Orange", bg="Black", variable=self.recursive_value, onvalue=1, offvalue=0)
		self.recursive.grid(row=0, column=2)

		self.fieldRow1.pack()

		# second field frame (inside main frame) config
		self.fieldRow2 = Frame(self.mainFrame, padx=5, pady=5, bg="Black")

		Label(self.fieldRow2, text="Remind me on :",fg="Orange", bg="Black", width=15).grid(row=0, column=0)
		self.day = Entry(self.fieldRow2, text=self.day_value, width=5, fg="Cyan", bg="Black")
		self.day.grid(row=0, column=1)
		
		Label(self.fieldRow2, text=":", fg="Orange", bg="Black").grid(row=0, column=2)
		self.month = AutocompleteCombobox(self.fieldRow2, text=self.month_value, width=10)
		self.month.set_completion_list(month_list)
		self.month.grid(row=0, column=3)
		
		Label(self.fieldRow2, text=":", fg="Orange", bg="Black").grid(row=0, column=4)
		self.year = Entry(self.fieldRow2, text=self.year_value, width=5, fg="Cyan", bg="Black")
		self.year.grid(row=0, column=5)
		self.fieldRow2.pack()

		# third field frame (inside main frame) config
		self.fieldRow3 = Frame(self.mainFrame, padx=5, pady=5, bg="Black")
		Label(self.fieldRow3, text="Remind me at :", width=15, fg="Orange", bg="Black").grid(row=0, column=0)
		self.hrs = Entry(self.fieldRow3, text=self.hrs_value, width=5, fg="Cyan", bg="Black")
		self.hrs.grid(row=0, column=1)
		Label(self.fieldRow3, text=":", fg="Orange", bg="Black").grid(row=0, column=2)
		self.mins = Entry(self.fieldRow3, text=self.mins_value, width=5, fg="Cyan", bg="Black")
		
		self.mins.grid(row=0, column=3)

		am_pm_list = ('AM', 'PM')
		self.am_pm = AutocompleteCombobox(self.fieldRow3, text=self.am_pm_value, width=5)
		self.am_pm.set_completion_list(am_pm_list)
		self.am_pm.grid(row=0, column=4)

		self.fieldRow3.pack()

		# button frame (inside main frame) config
		self.buttonFrame = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn1 = Button(self.buttonFrame, text="Save", command=self.saveReminder, fg="Orange", bg="Black").grid(row=0, column=0)
		self.btn2 = Button(self.buttonFrame, text="Cancel", command=self.cancelReminder, fg="Orange", bg="Black").grid(row=0, column=2)
		self.btn3 = Button(self.buttonFrame, text="List of Reminders", command=self.showListOfReminders, fg="Orange", bg="Black").grid(row=0, column=3)
		self.buttonFrame.grid_columnconfigure(1, minsize=10)
		self.buttonFrame.pack()

		self.buttonFrame2 = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn4 = Button(self.buttonFrame2, text="Delete", command=self.deleteReminder, fg="Orange", bg="Black").grid(row=0, column=0)
		self.btn5 = Button(self.buttonFrame2, text="Mark as Completed", command=self.markAsComplete, fg="Orange", bg="Black").grid(row=0, column=2)
		self.buttonFrame2.grid_columnconfigure(1, minsize=10)
		self.buttonFrame2.pack()

		self.root.bind('<Control-s>', lambda event: self.saveReminder())
		self.root.bind('<Alt-s>', lambda event: self.saveReminder())

		# self.t2 = ToggledFrame(self.mainFrame, text='Active Reminders', relief="raised", borderwidth=1)
		# self.t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

		# listbox_active_rem = Listbox(self.t2.sub_frame, height=10, width=50, fg="Orange", bg="Black")

		# with open(REM_FILE, 'r+') as f:
		# 	entries = json.loads(f.read())
		# 	for reminder in entries.get('reminders').items():
		# 		listbox_active_rem.insert(END, str(reminder[1].get('reminder') + '    \t[' + str(reminder[0]) +']'))
		# listbox_active_rem.pack()
		# listbox_active_rem.bind("<<ListboxSelect>>", self.list_selection_change_callback)


		# call mainloop of Tk object
		self.root.mainloop()


	# def list_selection_change_callback(self,event):
	# 	selection = event.widget.curselection()
	# 	if selection:
	# 		index = selection[0]
	# 		data = event.widget.get(index)
	# 		# Reminder(self.reminder)
	# 	print('data : ' + str(index) + ' : ' + str(data))
		
	# 	import re
	# 	rem_id = re.search('(.*)(\[)(.*)(\])', str(data)).group(3)
	# 	print(rem_id)

	# 	with open(REM_FILE, 'r+') as f:
	# 		reminders = json.loads(f.read())
	# 		x = reminders.get('reminders').get(rem_id)
	# 		print('to edit from list : ' + str(x))
	# 		rem_obj = (rem_id,x)
	# 		print('rem obj : ' + str(rem_obj))
	# 		self.openEditReminder(rem_obj)


	# def openEditReminder(self, rem_obj):
	# 	print('rem obj : ' + str(rem_obj))
		# 
		# self.rem.delete(0, END)
		# self.rem.insert(0,str(rem_obj[1].get('reminder')))
		# Reminder(rem_obj)


	def position_window(self):
		'''
		utiltiy function to position window 
		at top right corner
		'''
		# screen_width = self.root.winfo_xscreenwidth()
		# screen_height = self.root.winfo_screenheight()
		x = 100
		y = 100
		self.root.geometry('+%d+%d' % (x, y))


	def saveReminder(self):
		'''
		utility function to save reminder
		'''
		print('save reminder')
		reminder_text = self.rem.get("1.0",END).strip()
		# reminder_text = self.rem.get().strip()
		hrs = self.hrs.get().strip().zfill(2)
		mins = self.mins.get().strip().zfill(2)
		am_pm = self.am_pm.get().strip()
		year = self.year.get().strip()
		month = self.month.get().strip()
		day = self.day.get().strip().zfill(2)

		print('recursive alarm or not : ' + str(self.recursive_value.get()))
		# if self.recursive_value.get() == 1:
		# 	REM_FILE = "alarms.json"

		# update list of reminders
		with open(REM_FILE, 'r+') as f:
			reminders = json.loads(f.read())
			f.seek(0)
			now = datetime.datetime.now()
			import time
			timestamp = time.localtime() # get struct_time
			time_string = time.strftime("%m%d%H%M%S", timestamp)
			time_string = time_string
			print("timestamp =", time_string)
			if self.reminder_as_param:
				rem_creation_id = self.reminder_as_param[0]
			else:
				rem_creation_id = time_string
			if self.recursive_value.get() == 1:
				new_entry = {"creation time": str(now), "reminder": reminder_text, "time": hrs+":"+mins+":"+am_pm}
				reminders.get('alarms').update(new_entry)
			else:
				new_entry = {"creation time": str(now), "reminder": reminder_text, "date": day+"-"+month+"-"+year, "time": hrs+":"+mins+":"+am_pm}
				reminders.get('reminders').update({str(rem_creation_id):new_entry})
			f.write(json.dumps(reminders))
			f.truncate()

		self.root.destroy()
	
	def markAsComplete(self):
		print('mark as complete')


	def deleteReminder(self):
		print('delete reminder')
	

	def cancelReminder(self):
		'''
		utility function to close window
		'''
		import os
		self.root.destroy()
		sys.exit()

	def showListOfReminders(self):
		self.root.destroy()
		import my_list_of_reminder
		my_list_of_reminder.ListReminder()


if __name__ == "__main__":
	Reminder()