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
import traceback 
import sys 

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



class Reminder(object):

	def __init__(self, rem_tuple=None, type_of_entry='active_reminder'):

		self.root = Tk()
		self.root.title("Set reminder")
		self.root["bg"] = "Black"
		self.root.lift()
		self.root.attributes("-topmost", True)
		self.root.focus_set()
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
		print('current date_time : ' + str(now))
		
		self.repeat_value = IntVar()
		self.rem_value = StringVar()
		self.day_value= IntVar()
		self.month_value = StringVar()
		self.year_value = IntVar()
		self.hrs_value = IntVar()
		self.mins_value = IntVar()
		self.am_pm_value = StringVar()
		self.err_value = StringVar()
		self.day_of_mon_value= IntVar()
		self.alarm_type_selected = IntVar()
		self.mon_value = IntVar()
		self.tue_value = IntVar()
		self.wed_value = IntVar()
		self.thu_value = IntVar()
		self.fri_value = IntVar()
		self.sat_value = IntVar()
		self.sun_value = IntVar()

		if self.reminder_as_param:
			self.rem_value.set(self.reminder_as_param[1].get('reminder'))
			if self.reminder_as_param[1].get('date'):	#will be active reminder or completed reminder
				date_parts = self.reminder_as_param[1].get('date').split('-')
				self.day_value.set(str(date_parts[0]).zfill(2))
				self.month_value.set(str(date_parts[1]).zfill(2))
				self.year_value.set(str(date_parts[2]).zfill(2))
			else:	#will be alarm (daily/weekly/monthly)
				self.repeat_value.set(1)
				self.alarm_type_selected.set(1)
				self.day_value.set(str(now.day).zfill(2))
				self.month_value.set(month_list[now.month-1])
				self.year_value.set(now.year)
			time_parts = self.reminder_as_param[1].get('time').split(':')
			self.hrs_value.set(str(time_parts[0]).zfill(2))
			self.mins_value.set(str(time_parts[1]).zfill(2))
			self.am_pm_value.set(str(time_parts[2]).zfill(2))
			day_mon_value = self.reminder_as_param[1].get('day_of_month')
			day_of_week = self.reminder_as_param[1].get('day_of_week')
			if day_mon_value:
				self.day_of_mon_value.set(str(day_mon_value))
				self.alarm_type_selected.set(3)
			elif day_of_week:
				self.alarm_type_selected.set(2)
				if 'Mon' in day_of_week:
					self.mon_value.set(1)
				if 'Tue' in day_of_week:
					self.tue_value.set(1)
				if 'Wed' in day_of_week:
					self.wed_value.set(1)
				if 'Thu' in day_of_week:
					self.thu_value.set(1)
				if 'Fri' in day_of_week:
					self.fri_value.set(1)
				if 'Sat' in day_of_week:
					self.sat_value.set(1)
				if 'Sun' in day_of_week:
					self.sun_value.set(1)
			else:
				self.alarm_type_selected.set(1)
				self.day_of_mon_value.set(str(now.day).zfill(2))
				self.mon_value.set(0)
				self.tue_value.set(0)
				self.wed_value.set(0)
				self.thu_value.set(0)
				self.fri_value.set(0)
				self.sat_value.set(0)
				self.sun_value.set(0)
		else:
			self.repeat_value.set(0)
			self.day_value.set(str(now.day).zfill(2))
			self.month_value.set(month_list[now.month-1])
			self.year_value.set(now.year)
			if now.hour == 0 or now.hour == 12:
				hrs_in_analog = 12 
			else:
				hrs_in_analog = now.hour%12
			self.hrs_value.set(str(hrs_in_analog).zfill(2) )
			time_min = now.minute+1 if (now.minute+1) < 59 else 59
			self.mins_value.set(str(time_min).zfill(2))
			if now.hour >= 12:
				self.am_pm_value.set('PM')
			else:
				self.am_pm_value.set('AM')
			self.day_of_mon_value.set(str(now.day).zfill(2))
			self.alarm_type_selected.set(1)
		
		# main frame (inside root) config
		self.mainFrame = Frame(self.root, padx=10, pady = 10, bg="Black")
		self.mainFrame.pack(side=tkinter.LEFT)

		# first field frame (inside main frame) config
		self.fieldRow1 = Frame(self.mainFrame, padx=5, pady=5, bg="Black")
		
		Label(self.fieldRow1, text="Remind me \n about:", underline=12, fg="Orange", bg="Black").grid(row=0, column=0)
		self.rem = Text(self.fieldRow1, wrap=WORD, height=6, width=40, fg="Cyan", bg="Black")
		if self.reminder_as_param:
			self.rem.insert(END, self.rem_value.get())
		self.rem.grid(row=0, column=1)
		self.rem.focus_set() 
		self.rem.focus()
		self.rem.bind("<Tab>", self.focus_next_widget)

		self.repeat_alarm = Checkbutton(self.fieldRow1, text='Repeat', underline=0, command=self.alarm_checkbox_toggle, fg="Orange", bg="Black", variable=self.repeat_value, onvalue=1, offvalue=0)
		self.repeat_alarm.grid(row=0, column=2)

		self.fieldRow1.pack()

		# second field frame (inside main frame) config
		self.fieldRow2 = Frame(self.mainFrame, padx=5, pady=5, bg="Black")

		Label(self.fieldRow2, text="Remind me on :", underline=1, fg="Orange", bg="Black", width=15).grid(row=0, column=0)
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
		Label(self.fieldRow3, text="Remind me at :", underline=3, width=15, fg="Orange", bg="Black").grid(row=0, column=0)
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
		self.btn1 = Button(self.buttonFrame, text="Save", underline=0, command=self.saveReminder, fg="Orange", bg="Black").grid(row=0, column=0)
		self.btn2 = Button(self.buttonFrame, text="Cancel.", underline=6, command=self.cancelReminder, fg="Orange", bg="Black").grid(row=0, column=2)
		self.btn3 = Button(self.buttonFrame, text="List of Reminders",underline=0, command=self.showListOfReminders, fg="Orange", bg="Black").grid(row=0, column=3)
		self.buttonFrame.grid_columnconfigure(1, minsize=10)
		self.buttonFrame.pack()

		self.buttonFrame2 = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		if self.reminder_as_param:
			self.btn4 = Button(self.buttonFrame2, text="Delete", command=self.deleteReminder, fg="Orange", bg="Black").grid(row=0, column=0)
			if type_of_entry == 'active_reminder':
				self.btn5 = Button(self.buttonFrame2, text="Mark as Completed", command=self.markAsComplete, fg="Orange", bg="Black").grid(row=0, column=1)
		self.buttonFrame2.grid_columnconfigure(1, minsize=10)
		self.buttonFrame2.pack()

		self.errorFrame = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.error_label = Label(self.errorFrame, text="Error :"+str(self.err_value.get()), underline=1, fg="Orange", bg="Black")
		self.error_label.grid(row=1, column=0)
		self.errorFrame.pack()

		self.alarmFram = Frame(self.mainFrame, padx=5, pady=5, bg="Black")

		self.radiBouttonFrame = Frame(self.alarmFram, padx=10, pady=10, bg="Black")
		self.R1 = Radiobutton(self.radiBouttonFrame, text="Daily Alarm", underline=0, variable=self.alarm_type_selected, value=1, command=self.alarmTypeSelectionEvent, fg="Orange", bg="Black").grid(row=0, column=0)
		self.R2 = Radiobutton(self.radiBouttonFrame, text="Weekly Alarm", underline=0, variable=self.alarm_type_selected, value=2, command=self.alarmTypeSelectionEvent, fg="Orange", bg="Black").grid(row=0, column=1)
		self.R3 = Radiobutton(self.radiBouttonFrame, text="Monthly Alarm", underline=0, variable=self.alarm_type_selected, value=3, command=self.alarmTypeSelectionEvent, fg="Orange", bg="Black").grid(row=0, column=2)
		self.radiBouttonFrame.grid_columnconfigure(1, minsize=10)
		self.radiBouttonFrame.pack(side=TOP)

		self.monthlyAlarmFrame = Frame(self.alarmFram, padx=5, pady=5, bg="Black")
		Label(self.monthlyAlarmFrame, text="On day ", underline=1, fg="Orange", bg="Black", width=15).grid(row=0, column=0)
		self.day_of_mon = Entry(self.monthlyAlarmFrame, text=self.day_of_mon_value, width=5, fg="Cyan", bg="Black")
		self.day_of_mon.grid(row=0, column=1)
		Label(self.monthlyAlarmFrame, text="of every Month ",fg="Orange", bg="Black", width=15).grid(row=0, column=2)
		self.monthlyAlarmFrame.grid_columnconfigure(2, minsize=10)
		if self.alarm_type_selected.get() == 3:
			self.monthlyAlarmFrame.pack(side=BOTTOM)
		if self.repeat_value.get():
			self.alarmFram.pack()

		self.weeklyAlarmFrame = Frame(self.alarmFram, padx=5, pady=5, bg="Black")
		self.weekday_1 = Checkbutton(self.weeklyAlarmFrame, text='1. Monday', underline=0, fg="Orange", bg="Black", variable=self.mon_value)
		self.weekday_1.grid(row=0, column=1)
		self.weekday_2 = Checkbutton(self.weeklyAlarmFrame, text='2. Tuesday', underline=0, fg="Orange", bg="Black", variable=self.tue_value)
		self.weekday_2.grid(row=0, column=2)
		self.weekday_3 = Checkbutton(self.weeklyAlarmFrame, text='3. Wednesday', underline=0, fg="Orange", bg="Black", variable=self.wed_value)
		self.weekday_3.grid(row=0, column=3)
		self.weekday_4 = Checkbutton(self.weeklyAlarmFrame, text='4. Thursday',  underline=0, fg="Orange", bg="Black", variable=self.thu_value)
		self.weekday_4.grid(row=1, column=1)
		self.weekday_5 = Checkbutton(self.weeklyAlarmFrame, text='5. Friday',  underline=0, fg="Orange", bg="Black", variable=self.fri_value)
		self.weekday_5.grid(row=1, column=2)
		self.weekday_6 = Checkbutton(self.weeklyAlarmFrame, text='6. Saturday',  underline=0, fg="Orange", bg="Black", variable=self.sat_value)
		self.weekday_6.grid(row=1, column=3)
		self.weekday_7 = Checkbutton(self.weeklyAlarmFrame, text='7. Sunday',  underline=0, fg="Orange", bg="Black", variable=self.sun_value)
		self.weekday_7.grid(row=2, column=2)
		self.weeklyAlarmFrame.grid_columnconfigure(2, minsize=10)

		if self.alarm_type_selected.get() == 2:
			self.weeklyAlarmFrame.pack(side=BOTTOM)
		if self.repeat_value.get():
			self.alarmFram.pack()

		self.root.bind('<Alt-l>', lambda event: self.showListOfReminders())
		self.root.bind('<Alt-s>', lambda event: self.saveReminder())
		self.root.bind('<Alt-r>', lambda event: self.toggleRepeat_alarm())
		self.root.bind('<Alt-.>', lambda event: self.cancelReminder())
		self.root.bind('<Alt-m>', lambda event: self.selectMonthlyAlarm())
		self.root.bind('<Alt-w>', lambda event: self.selectWeeklyAlarm())
		self.root.bind('<Alt-d>', lambda event: self.selectDailyAlarm())
		self.root.bind('<Alt-e>', lambda event: self.focusOnDateField()) #reminde me on 
		self.root.bind('<Alt-i>', lambda event: self.focusOnTimeField())
		self.root.bind('<Alt-a>', lambda event: self.focusRemTextField())
		self.root.bind('<Alt-n>', lambda event: self.focusOnDayOfMonthField())

		self.root.bind('<Alt-KeyPress-1>', lambda event: self.selectWeekday(self.mon_value))
		self.root.bind('<Alt-KeyPress-2>', lambda event: self.selectWeekday(self.tue_value))
		self.root.bind('<Alt-KeyPress-3>', lambda event: self.selectWeekday(self.wed_value))
		self.root.bind('<Alt-KeyPress-4>', lambda event: self.selectWeekday(self.thu_value))
		self.root.bind('<Alt-KeyPress-5>', lambda event: self.selectWeekday(self.fri_value))
		self.root.bind('<Alt-KeyPress-6>', lambda event: self.selectWeekday(self.sat_value))
		self.root.bind('<Alt-KeyPress-7>', lambda event: self.selectWeekday(self.sun_value))

		if self.reminder_as_param:	#to bring the the window on top of others
			self.root.iconify()
			self.root.update()
			self.root.deiconify()
		
		self.root.mainloop()

	def focusOnTimeField(self):
		self.hrs.focus_set() 
		self.hrs.select_range(0,END)

	def focusRemTextField(self):
		self.rem.focus_set() 
		self.rem.tag_add(0,END) 

	def focusOnDateField(self):
		self.day.focus_set() 
		self.day.select_range(0,END) 

	def focusOnDayOfMonthField(self):
		self.day_of_mon.focus_set() 
		self.day_of_mon.select_range(0,END) 

	def alarm_checkbox_toggle(self):
		if bool(self.repeat_value.get()):
			self.alarmFram.pack()
		else:
			self.alarmFram.forget()

	def toggleRepeat_alarm(self):
		if bool(self.repeat_value.get()):
			self.repeat_alarm.deselect()
		else:
			self.repeat_alarm.select()
		self.alarm_checkbox_toggle()

	def alarmTypeSelectionEvent(self):
		if self.alarm_type_selected.get() == 3:
			self.monthlyAlarmFrame.pack()
			self.weeklyAlarmFrame.forget()
		elif self.alarm_type_selected.get() == 2:
			self.weeklyAlarmFrame.pack()
			self.monthlyAlarmFrame.forget()
		elif self.alarm_type_selected.get() == 1:
			self.weeklyAlarmFrame.forget()
			self.monthlyAlarmFrame.forget()

	def selectWeekday(self, day_selected):
		if day_selected.get():
			day_selected.set(0)
		else:
			day_selected.set(1)

	def selectMonthlyAlarm(self):
		self.alarm_type_selected.set(3)
		self.alarmTypeSelectionEvent()

	def selectWeeklyAlarm(self):
		self.alarm_type_selected.set(2)
		self.alarmTypeSelectionEvent()

	def selectDailyAlarm(self):
		self.alarm_type_selected.set(1)
		self.alarmTypeSelectionEvent()

	def focus_next_widget(self, event):
		event.widget.tk_focusNext().focus()
		return("break")

	def openEditReminder(self, rem_obj):
		print('rem obj : ' + str(rem_obj))
		
		self.rem.delete(0, END)
		self.rem.insert(0,str(rem_obj[1].get('reminder')))
		Reminder(rem_obj)

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
		invalid_entry = False
		error_string = ''

		def get_datetime_obj_from_str(date_time_str):
			try:
				import datetime
				reminder_datetime_obj = datetime.datetime.strptime(date_time_str,'%d-%B-%Y %I:%M:%p')
				return reminder_datetime_obj
			except Exception as e:
				invalid_entry = True
				error_string = 'Please enter correct date and time...'
				traceback.print_exception(*sys.exc_info())
		
		print('save reminder called')
		reminder_text = self.rem.get("1.0",END).strip()
		hrs = self.hrs.get().strip().zfill(2)
		mins = self.mins.get().strip().zfill(2)
		am_pm = self.am_pm.get().strip()
		year = self.year.get().strip()
		month = self.month.get().strip()
		day = self.day.get().strip().zfill(2)
		if self.alarm_type_selected.get() == 3:
			day_of_mon = self.day_of_mon.get().strip().zfill(2)

		if reminder_text == "":
			invalid_entry = True
			error_string = 'Please add content for reminder...'
		now = datetime.datetime.now()
		cur_datetime = str(now.strftime("%d-%B-%Y %I:%M:%p")).strip()
		cur_datetime_obj = datetime.datetime.strptime(cur_datetime,'%d-%B-%Y %I:%M:%p')
		
		date_time_str = day+"-"+month+"-"+year + " " + hrs+":"+mins+":"+am_pm
		date_time_obj = get_datetime_obj_from_str(date_time_str)
		if not date_time_obj or date_time_obj < cur_datetime_obj:
			invalid_entry = True
			error_string = 'Please set proper date and time for reminder...'

		# update list of reminders
		with open(REM_FILE, 'r+') as f:
			reminders = json.loads(f.read())
			f.seek(0)
			now = datetime.datetime.now()
			import time
			timestamp = time.localtime() # get time
			time_string = time.strftime("%m%d%H%M%S", timestamp)
			time_string = time_string
			if self.reminder_as_param:
				rem_creation_id = self.reminder_as_param[0]
			else:
				rem_creation_id = time_string
			print('repeat_alarm or not : ' + str(self.repeat_value.get()))
			if self.repeat_value.get() == 1:
				if self.alarm_type_selected.get() == 1:
					new_entry = {"creation time": str(now), "reminder": reminder_text, "time": hrs+":"+mins+":"+am_pm, "last_executed":str(int(day)-1 if int(day)>1 else 1)+"-"+month+"-"+year, "snooze":0}
					reminders.get('daily_alarms').update({str(rem_creation_id):new_entry})
					if reminders.get('monthly_alarms').get(rem_creation_id):
						reminders.get('monthly_alarms').pop(rem_creation_id)
					if reminders.get('weekly_alarms').get(rem_creation_id):
						reminders.get('weekly_alarms').pop(rem_creation_id)
				elif self.alarm_type_selected.get() == 2:
					days_of_week = []
					days_of_week.append("Mon") if self.mon_value.get() else print('Monday not selected')
					days_of_week.append("Tue") if self.tue_value.get() else print('Tuesday not selected')
					days_of_week.append("Wed") if self.wed_value.get() else print('Wednesday not selected')
					days_of_week.append("Thu") if self.thu_value.get() else print('Thursday not selected')
					days_of_week.append("Fri") if self.fri_value.get() else print('Friday not selected')
					days_of_week.append("Sat") if self.sat_value.get() else print('Saturday not selected')
					days_of_week.append("Sun") if self.sun_value.get() else print('Sunday not selected')
					print("slected days of week : ", str(days_of_week))
					if days_of_week:
						new_entry = {"creation time": str(now), "reminder": reminder_text, "day_of_week":days_of_week, "time": hrs+":"+mins+":"+am_pm, "last_executed":str(int(day)-1 if int(day)>1 else 1)+"-"+month+"-"+year, "snooze":0}
						reminders.get('weekly_alarms').update({str(rem_creation_id):new_entry})
						if reminders.get('monthly_alarms').get(rem_creation_id):
							reminders.get('monthly_alarms').pop(rem_creation_id)
						if reminders.get('daily_alarms').get(rem_creation_id):
							reminders.get('daily_alarms').pop(rem_creation_id)
					else:
						invalid_entry = True
						error_string = 'Please select a day of week at least'
				elif self.alarm_type_selected.get() == 3: 
					if int(day_of_mon)>0:
						new_entry = {"creation time": str(now), "reminder": reminder_text, "day_of_month":day_of_mon, "time": hrs+":"+mins+":"+am_pm, "last_executed":str(int(day)-1 if int(day)>1 else 1)+"-"+month+"-"+year, "snooze":0}
						reminders.get('monthly_alarms').update({str(rem_creation_id):new_entry})
						if reminders.get('daily_alarms').get(rem_creation_id):
							reminders.get('daily_alarms').pop(rem_creation_id)
						if reminders.get('weekly_alarms').get(rem_creation_id):
							reminders.get('weekly_alarms').pop(rem_creation_id)
					else:
						invalid_entry = True
						error_string = 'Enter a valid day of month for monthly alarm!!'
					
				if reminders.get('reminders').get(rem_creation_id):
					reminders.get('reminders').pop(rem_creation_id)
				if reminders.get('completed_reminders').get(rem_creation_id):
					reminders.get('completed_reminders').pop(rem_creation_id)
			else:	#not repeat alarm
				new_entry = {"creation time": str(now), "reminder": reminder_text, "date": day+"-"+month+"-"+year, "time": hrs+":"+mins+":"+am_pm}
				reminders.get('reminders').update({str(rem_creation_id):new_entry})
				if reminders.get('completed_reminders').get(rem_creation_id):
					reminders.get('completed_reminders').pop(rem_creation_id)
				if reminders.get('daily_alarms').get(rem_creation_id):
					reminders.get('daily_alarms').pop(rem_creation_id)

				if reminders.get('monthly_alarms').get(rem_creation_id):
					reminders.get('monthly_alarms').pop(rem_creation_id)
			
			if not invalid_entry:
				f.write(json.dumps(reminders))
				f.truncate()

			if invalid_entry:
				print(error_string)
				self.err_value.set(error_string)
				self.error_label.configure(text="Error :"+str(self.err_value.get()))
				self.error_label.update()
			else:
				self.root.destroy()

	def markAsComplete(self):
		'''
		utitlity function to mark reminder as complete
		'''
		try:
			print('mark as complete called')
			# move the active reminder to completed ones
			with open(REM_FILE, 'r+') as f:
				reminders = json.loads(f.read())
				x = reminders.get('reminders').pop(self.reminder_as_param[0])
				print('completed : ' + str(x))
				reminders.get('completed_reminders').update({self.reminder_as_param[0]:x})
			# write the updated values
			with open(REM_FILE, 'w') as f:
				f.write(json.dumps(reminders))
	
			self.root.destroy()
			print('destroy called\n')
		except Exception as e:
			traceback.print_exception(*sys.exc_info())

	def deleteReminder(self):
		'''
		utitlity function to delete reminder
		'''
		try:
			print('delete reminder called')
			with open(REM_FILE, 'r+') as f:
				reminders = json.loads(f.read())
				x = None
				if reminders.get('reminders').get(self.reminder_as_param[0]):
					x = reminders.get('reminders').pop(self.reminder_as_param[0])
				elif reminders.get('completed_reminders').get(self.reminder_as_param[0]):
					x = reminders.get('completed_reminders').pop(self.reminder_as_param[0])
				elif reminders.get('daily_alarms').get(self.reminder_as_param[0]):
					x = reminders.get('daily_alarms').pop(self.reminder_as_param[0])
			# write the updated values
			with open(REM_FILE, 'w') as f:
				f.write(json.dumps(reminders))
	
			self.root.destroy()
			print('destroy called\n')
		except Exception as e:
			traceback.print_exception(*sys.exc_info())

	def cancelReminder(self):
		'''
		utility function to close window
		'''
		print('cancel reminder called')
		import os
		import sys
		self.root.destroy()
		# sys.exit()	- this can't be used as it may kill the process itself.

	def showListOfReminders(self):
		self.root.destroy()
		import my_list_of_reminder
		my_list_of_reminder.ListReminder('from_reminder_create_from')


if __name__ == "__main__":
	Reminder()
