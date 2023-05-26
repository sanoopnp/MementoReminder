try:
	# for Python2
	from Tkinter import *
except ImportError:
	# for Python3
	from tkinter import *
	from tkinter import font
from datetime import datetime
import time
import json
import my_reminder_create_form

# path to reminders.json file
REM_FILE = "reminders.json"

# list of reminders
reminders = []


class ShowReminder():
	def __init__(self, reminder):
		# reminder info tuple
		self.reminder = reminder
		print('ShowReminder gets called' + str(self.reminder) + '\n')

		# root (top level element) config
		self.root = Tk()
		self.root.title("Reminder!")
		self.root["bg"] = "Black"
		self.position_window()
		self.root.geometry("550x350")
		self.root.resizable(True, True)

		# main frame (inside root) config
		self.mainFrame = Frame(self.root, padx=10, pady = 10, bg="DarkKhaki") #DarkKhaki, Olive, Yellow, Teal, turquoise, chocolate
		self.mainFrame.pack(side="bottom", fill=BOTH, expand=1)

		# reminder labelFrame (inside main frame) config
		self.labelFrame = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.text = Label(self.labelFrame, text=self.reminder[1].get('reminder'), bg="Black",
					font = font.Font(family="Times", size=18), fg="Orange",
					padx=20, pady=10, wraplength=500).grid(row=0, column=1)
		self.date_time_of_trigger = Label(self.labelFrame, text=self.reminder[1].get('date') + " " + self.reminder[1].get('time') , bg="Black",
					font = font.Font(family="Times", size=12), fg="Orange",
					padx=20, pady=10, wraplength=300).grid(row=1, column=1)
		self.labelFrame.grid_columnconfigure(3, minsize=10)
		# self.labelFrame.pack()
		
		# button frame1 (inside main frame) config
		self.buttonRow = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn12 = Button(self.buttonRow, text="Show", command=self.showContent, fg="Orange", bg="Black").grid(row=0, column=1)
		self.btn1 = Button(self.buttonRow, text="Dismiss", underline="0", command=self.dismissReminder, fg="Orange", bg="Black").grid(row=0, column=1)
		self.btn2 = Button(self.buttonRow, text="Edit", underline="0" , command=self.editReminder, fg="Orange", bg="Black").grid(row=0, column=2)
		self.btn22 = Button(self.buttonRow, text="Put To Silence", underline="0" , command=self.putToSilence, fg="Orange", bg="Black").grid(row=0, column=3)
		self.buttonRow.grid_columnconfigure(3, minsize=10)
		self.buttonRow.pack()
		
		# button frame2 (inside main frame) config
		self.buttonRow2 = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn3 = Button(self.buttonRow2, text="Remind in 10", underline="11", command=self.remindIn10, fg="Orange", bg="Black").grid(row=0, column=1)
		self.btn4 = Button(self.buttonRow2, text="Remind in an hour[L]", underline="18", command=self.remindInHour, fg="Orange", bg="Black").grid(row=0, column=2)
		self.btn4_5 = Button(self.buttonRow2, text="Remind in 6 hours[M]", underline="18", command=self.remindIn6Hours, fg="Orange", bg="Black").grid(row=0, column=3)
		self.btn5 = Button(self.buttonRow2, text="Remind in 12 hours[K]", underline="19", command=self.remindIn12Hours, fg="Orange", bg="Black").grid(row=0, column=4)
		self.buttonRow2.grid_columnconfigure(3, minsize=10)
		self.buttonRow2.pack()
		
		# button frame3 (inside main frame) config
		self.buttonRow3 = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn6 = Button(self.buttonRow3, text="Remind me T'moro", underline='10', command=self.remindTomorrow, fg="Orange", bg="Black").grid(row=0, column=1)
		self.btn7 = Button(self.buttonRow3, text="Remind in 2 Days ", command=self.remindIn2Days, fg="Orange", bg="Black").grid(row=0, column=2)
		self.btn8 = Button(self.buttonRow3, text="Remind in 3 Days", command=self.remindIn3Days, fg="Orange", bg="Black").grid(row=0, column=3)
		self.buttonRow3.grid_columnconfigure(3, minsize=10)
		self.buttonRow3.pack()

		# button frame3 (inside main frame) config
		self.buttonRow4 = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn9 = Button(self.buttonRow4, text="Remind in a Week", command=self.remindInWeek, fg="Orange", bg="Black").grid(row=0, column=1)
		self.btn10 = Button(self.buttonRow4, text="Remind in a Month", command=self.remindInMonth, fg="Orange", bg="Black").grid(row=0, column=2)
		self.btn11 = Button(self.buttonRow4, text="Remind in 3 Months", command=self.remind3Months, fg="Orange", bg="Black").grid(row=0, column=3)
		self.buttonRow4.grid_columnconfigure(3, minsize=10)
		self.buttonRow4.pack()


		self.root.lift()
		self.root.attributes("-topmost", True)
		self.root.bind('<Alt-d>', lambda event: self.dismissReminder())
		self.root.bind('<Alt-s>', lambda event: self.showContent())
		self.root.bind('<Alt-p>', lambda event: self.putToSilence())
		self.root.bind('<Alt-0>', lambda event: self.remindIn10())
		self.root.bind('<Alt-l>', lambda event: self.remindInHour())
		self.root.bind('<Alt-m>', lambda event: self.remindIn6Hours())
		self.root.bind('<Alt-k>', lambda event: self.remindIn12Hours())
		self.root.bind('<Alt-t>', lambda event: self.remindTomorrow())
		# self.root.bind('<Alt-2>', lambda event: self.remindIn2Days())
		# self.root.bind('<Alt-3>', lambda event: self.remindIn3Days())
		self.root.update()
		self.root.focus_force()
		# print('self.labelFrame die : ' + str(self.labelFrame.winfo_width()) + ' X ' + str(self.labelFrame.winfo_height()))
		if self.labelFrame.winfo_height() > 150:
			ht = self.labelFrame.winfo_height() + 200
			self.root.geometry(f"550x{ht}")
		# call mainloop of Tk object
		self.root.mainloop()

	def position_window(self):
		'''
		utiltiy function to position window 
		at top right corner
		'''
		x = 100
		y = 100
		self.root.geometry('+%d+%d' % (x, y))

	def showContent(self):
		self.labelFrame.pack()

	def dismissReminder(self):
		'''
		utitlity function to remove reminder form list
		'''
		# move the active reminder to completed ones
		with open(REM_FILE, 'r+') as f:
			reminders = json.loads(f.read())
			x = reminders.get('reminders').pop(self.reminder[0])
			reminders.get('completed_reminders').update({self.reminder[0]:x})
			print('reminder removed from active and added to completed : ' + str(x))

		# write the updated values
		with open(REM_FILE, 'w') as f:
			f.write(json.dumps(reminders))

		self.root.destroy()
		print('reminder dismissed and destroy called\n')

	def postpone_for(self, time_in_mins):
		'''
		utility function to postpone reminder by 10 minutes
		'''
		
		import datetime
		with open(REM_FILE, 'r+') as f:
			reminders = json.loads(f.read())
			# print('reminders before postpone : ' + str(reminders))
			x = reminders.get('reminders').get(self.reminder[0])
			reminder_obj = (str(self.reminder[0]),x)
			# print('reminder to be postponed :' + str(reminder_obj))
			# reminder_datetime_obj = get_datetime_obj_from_str(reminder_obj)
			import datetime
			now = datetime.datetime.now()
			cur_datetime = str(now.strftime("%d-%B-%Y %I:%M:%p")).strip()
			cur_datetime_obj = datetime.datetime.strptime(cur_datetime,'%d-%B-%Y %I:%M:%p')
			new_time = cur_datetime_obj + datetime.timedelta(minutes = time_in_mins)
			new_format = new_time.strftime("%d-%B-%Y %I:%M:%p").split(' ')
			y = {
				'reminder':x.get('reminder'),
				'date': str(new_format[0]),
				'time': str(new_format[1])
			}
			new_reminder_obj = (str(self.reminder[0]),y)
			reminders.get('reminders').update({self.reminder[0]:y})
			# print('reminders after postpone : ' + str(reminders))
		
		#write back updated time for the reminder
		with open(REM_FILE, 'w') as f:
			f.write(json.dumps(reminders))

		self.root.destroy()
		print('reminder postponed and destroy called\n')

	def remindIn10(self):
		'''
		utility function to postpone reminder by 10 minutes
		'''
		self.postpone_for(10)

	def remindInHour(self):
		'''
		utility function to postpone reminder by 1 hour
		'''
		self.postpone_for(60)

	def remindIn12Hours(self):
		'''
		utility function to postpone reminder by 1 day
		'''
		self.postpone_for(60*12)
		
	def remindIn6Hours(self):
		'''
		utility function to postpone reminder by 1 day
		'''
		self.postpone_for(60*6)

	def remindTomorrow(self):
		'''
		utility function to postpone reminder by 1 day
		'''
		self.postpone_for(60*24)

	def remindIn2Days(self):
		'''
		utility function to postpone reminder by 1 day
		'''
		self.postpone_for(60*24*2)

	def remindIn3Days(self):
		'''
		utility function to postpone reminder by 1 day
		'''
		self.postpone_for(60*24*3)

	def remindInWeek(self):
		'''
		utility function to postpone reminder after a week
		'''
		self.postpone_for(60*24*7)

	def remindInMonth(self):
		'''
		utility function to postpone reminder after a month
		'''
		self.postpone_for(60*24*30)

	def remind3Months(self):
		'''
		utility function to postpone reminder after 3 months
		'''
		self.postpone_for(60*24*30*3)

	def editReminder(self):
		'''
		utility function to edit reminder
		'''
		print('self.reminder object for edit reminder : ' + str(self.reminder))
		self.root.destroy()

		type_of_entry = 'active_reminder'
		my_reminder_create_form.Reminder(self.reminder, type_of_entry)

	def putToSilence(self):
		'''
		utility function to put the reminder to silence
		'''
		global silence_timeout
		print('self.putToSilence invoked from : reminder popup')
		type_of_entry = 'active_reminder'
		self.my_reminder_silence_form=PutToSilence(self.root)
		self.my_reminder_silence_form.top.wait_window()
		silence_timeout = int(self.my_reminder_silence_form.value)
		print('value got for silence_timeout : reminder popup ' + str(silence_timeout))


class PutToSilence(object):
	def __init__(self,root):
		self.value='0'
		top=self.top=Toplevel(root)
		self.l=Label(top, text="Put to Silence for <x> hours :", fg="Orange", bg="Black", width=25)
		self.l.pack()
		self.e=Entry(top)
		self.e.pack()
		self.e.focus_set()
		self.b=Button(top, text="Save", underline=0, command=self.cleanup, fg="Orange", bg="Black")
		self.b.pack()
		self.top["bg"] = "Black"
		self.top.attributes('-topmost',1)
		self.top.bind('<Alt-s>', lambda event: self.cleanup())
		WIDTH = 250
		HEIGHT = 80
		lv_x = 250
		lv_y = 150
		self.top.geometry(f'{WIDTH}x{HEIGHT}+{lv_x}+{lv_y}')
	def cleanup(self):
		self.value=self.e.get()
		self.top.destroy()


class ShowAlarm():
	def __init__(self, reminder, alarm_type):
		# reminder info tuple
		self.reminder = reminder
		print('ShowAlarm gets called' + str(self.reminder) + '\n')

		# root (top level element) config
		self.root = Tk()
		self.root.title(alarm_type + " Alarm!")
		self.root["bg"] = "Black"
		self.position_window()
		self.root.geometry("550x300")
		self.root.resizable(True, True)

		# main frame (inside root) config
		self.mainFrame = Frame(self.root, width=100, height=100, padx=10, pady = 10, bg="Black")
		self.mainFrame.pack(side="bottom", fill=None, expand=0)

		# reminder labelFrame (inside main frame) config
		self.labelFrame = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.text = Label(self.labelFrame, text=self.reminder[1].get('reminder'), bg="Black", 
					font = font.Font(family="Times", size=18), fg="Orange", 
					padx=20, pady=10, wraplength=500).grid(row=0, column=1)
		self.date_time_of_trigger = Label(self.labelFrame, text='Scheduled @:' + self.reminder[1].get('time') , bg="Black", 
					font = font.Font(family="Times", size=12), fg="Orange", 
					padx=20, pady=10, wraplength=300).grid(row=1, column=1)
		
		self.labelFrame.grid_columnconfigure(3, minsize=10)
		# self.labelFrame.pack()

		# button frame1 (inside main frame) config
		self.buttonRow_1 = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn7 = Button(self.buttonRow_1, text="Show", underline=0, command=self.showContent, fg="Orange", bg="Black").grid(row=0, column=0)
		self.btn1 = Button(self.buttonRow_1, text="Dismiss", underline=0, command=self.dismissAlarm, fg="Orange", bg="Black").grid(row=0, column=0)
		self.btn2 = Button(self.buttonRow_1, text="Edit", underline=0, command=self.editAlarm, fg="Orange", bg="Black").grid(row=0, column=1)
		self.btn22 = Button(self.buttonRow_1, text="Put To Silence", underline="0" , command=self.putToSilence, fg="Orange", bg="Black").grid(row=0, column=3)
		self.btn3 = Button(self.buttonRow_1, text="Snooze 10", underline=8, command= lambda: self.snoozeAlarm(10), fg="Orange", bg="Black").grid(row=0, column=4)
		self.buttonRow_1.grid_columnconfigure(3, minsize=10)
		self.buttonRow_1.pack()
		
		# button frame2 (inside main frame) config
		self.buttonRow_2 = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn4 = Button(self.buttonRow_2, text="Snooze 30 [M]", underline=11, command=lambda: self.snoozeAlarm(30), fg="Orange", bg="Black").grid(row=0, column=0)
		self.btn5 = Button(self.buttonRow_2, text="Hour Snooze [L]", underline=13, command=lambda: self.snoozeAlarm(60), fg="Orange", bg="Black").grid(row=0, column=1)
		self.btn6 = Button(self.buttonRow_2, text="Snooze 2 Hours [K]", underline=16, command= lambda: self.snoozeAlarm(120), fg="Orange", bg="Black").grid(row=0, column=2)
		self.buttonRow_2.grid_columnconfigure(3, minsize=10)
		self.buttonRow_2.pack()

		# button frame3 (inside main frame) config
		self.buttonRow_3 = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn8 = Button(self.buttonRow_3, text="Snooze 12 Hours [O]", underline=11, command=lambda: self.snoozeAlarm(60*12), fg="Orange", bg="Black").grid(row=0, column=0)
		self.btn9 = Button(self.buttonRow_3, text="Snooze 1 Day [U]",  command=lambda: self.snoozeAlarm(60*24), fg="Orange", bg="Black").grid(row=0, column=1)
		self.btn10 = Button(self.buttonRow_3, text="Snooze 2 Days [N]", underline=1, command= lambda: self.snoozeAlarm(60*48), fg="Orange", bg="Black").grid(row=0, column=2)
		self.buttonRow_3.grid_columnconfigure(3, minsize=10)
		self.buttonRow_3.pack()

		self.root.lift()
		self.root.attributes("-topmost", True)
		self.root.bind('<Alt-d>', lambda event: self.dismissAlarm())
		self.root.bind('<Alt-s>', lambda event: self.showContent())
		self.root.bind('<Alt-p>', lambda event: self.putToSilence())
		self.root.bind('<Alt-e>', lambda event: self.editAlarm())
		
		self.root.bind('<Alt-0>', lambda event: self.snoozeAlarm(10))
		self.root.bind('<Alt-m>', lambda event: self.snoozeAlarm(30))
		self.root.bind('<Alt-l>', lambda event: self.snoozeAlarm(60))
		self.root.bind('<Alt-k>', lambda event: self.snoozeAlarm(120))
		
		self.root.update()
		self.root.focus_force()
		# print('self.labelFrame die : ' + str(self.labelFrame.winfo_width()) + ' X ' + str(self.labelFrame.winfo_height()))
		if self.labelFrame.winfo_height() > 150:
			ht = self.labelFrame.winfo_height() + 120
			self.root.geometry(f"550x{ht}")
		# call mainloop of Tk object
		self.root.mainloop()

	def position_window(self):
		'''
		utiltiy function to position window 
		at top right corner
		'''
		x = 100
		y = 100
		self.root.geometry('+%d+%d' % (x, y))

	def showContent(self):
		self.labelFrame.pack()

	def dismissAlarm(self):
		'''
		utitlity function to remove alarm form list
		'''
		# update the last_executed date to current date
		with open(REM_FILE, 'r+') as f:
			reminders = json.loads(f.read())
			import datetime
			now = datetime.datetime.now()
			if reminders.get('daily_alarms').get(self.reminder[0]):
				x = reminders.get('daily_alarms').pop(self.reminder[0])
				cur_date = str(now.strftime("%d-%B-%Y")).strip()
				x.update({'last_executed':cur_date})
				x.update({'snooze':0})
				reminders.get('daily_alarms').update({self.reminder[0]:x})
			elif reminders.get('monthly_alarms').get(self.reminder[0]):
				x = reminders.get('monthly_alarms').pop(self.reminder[0])
				cur_date = str(now.strftime("%d-%B-%Y")).strip()
				x.update({'last_executed':cur_date})
				x.update({'snooze':0})
				reminders.get('monthly_alarms').update({self.reminder[0]:x})
			elif reminders.get('weekly_alarms').get(self.reminder[0]):
				x = reminders.get('weekly_alarms').pop(self.reminder[0])
				cur_date = str(now.strftime("%d-%B-%Y")).strip()
				x.update({'last_executed':cur_date})
				x.update({'snooze':0})
				reminders.get('weekly_alarms').update({self.reminder[0]:x})

		# write the updated values
		with open(REM_FILE, 'w') as f:
			f.write(json.dumps(reminders))

		self.root.destroy()
		print('alarm dismissed and destroy called\n')

	def editAlarm(self):
		'''
		utility function to edit reminder
		'''
		print('self.reminder object for edit Alarm : ' + str(self.reminder))
		self.root.destroy()
		type_of_entry = 'daily_alarm'
		if self.reminder[1].get('day_of_week'):
			type_of_entry = 'weekly_alarm'
		if self.reminder[1].get('day_of_month'):
			type_of_entry = 'monthly_alarm'
		my_reminder_create_form.Reminder(self.reminder, type_of_entry)
	
	def snoozeAlarm(self, snooze_for):
		'''
		utility function to edit reminder
		'''

		def get_time_obj(rem_obj):
			import datetime
			alarm_time = str(rem_obj.get('time')).strip()
			alarm_time_obj = datetime.datetime.strptime(alarm_time,'%I:%M:%p')
			return alarm_time_obj

		def get_time_till_now(get_time_obj, x, cur_time_obj, cur_snooze):
			alarm_time_obj = get_time_obj(x)
			time_diff = cur_time_obj - alarm_time_obj
			time_diff_till_now = round(time_diff.total_seconds() / 60)
			print("time_diff_till_now : ", time_diff_till_now)
			cur_snooze = time_diff_till_now
			return cur_snooze

		import datetime
		now = datetime.datetime.now()
		cur_time = str(now.strftime("%I:%M:%p")).strip()
		cur_time_obj =  datetime.datetime.strptime(cur_time,'%I:%M:%p')

		snooze_length = snooze_for

		with open(REM_FILE, 'r+') as f:
			reminders = json.loads(f.read())
			if reminders.get('daily_alarms').get(self.reminder[0]):
				x = reminders.get('daily_alarms').pop(self.reminder[0])
				cur_snooze = x.get('snooze')
				if cur_snooze == 0:
					cur_snooze = get_time_till_now(get_time_obj, x, cur_time_obj, cur_snooze)
				next_snooze_time = cur_snooze + snooze_length
				print('next_snooze_time daily_alarms : ' + str(next_snooze_time))
				x.update({'snooze':next_snooze_time})
				reminders.get('daily_alarms').update({self.reminder[0]:x})
			elif reminders.get('monthly_alarms').get(self.reminder[0]):
				x = reminders.get('monthly_alarms').pop(self.reminder[0])
				cur_snooze = x.get('snooze')
				if cur_snooze == 0:
					cur_snooze = get_time_till_now(get_time_obj, x, cur_time_obj, cur_snooze)
				next_snooze_time = cur_snooze + snooze_length
				print('next_snooze_time monthly_alarms: ' + str(next_snooze_time))
				x.update({'snooze':next_snooze_time})
				reminders.get('monthly_alarms').update({self.reminder[0]:x})
			elif reminders.get('weekly_alarms').get(self.reminder[0]):
				x = reminders.get('weekly_alarms').pop(self.reminder[0])
				cur_snooze = x.get('snooze')
				if cur_snooze == 0:
					cur_snooze = get_time_till_now(get_time_obj, x, cur_time_obj, cur_snooze)
				next_snooze_time = cur_snooze + snooze_length
				print('next_snooze_time weekly_alarms: ' + str(next_snooze_time))
				x.update({'snooze':next_snooze_time})
				reminders.get('weekly_alarms').update({self.reminder[0]:x})

		# write the updated values
		with open(REM_FILE, 'w') as f:
			f.write(json.dumps(reminders))

		self.root.destroy()
		print('alarm snoozed and destroy called\n')

	def putToSilence(self):
		'''
		utility function to put the alarm to silence
		'''
		global silence_timeout
		print('self.putToSilence invoked from : alarm popup')
		type_of_entry = 'alarms'
		self.my_alarm_silence_form=PutToSilence(self.root)
		self.my_alarm_silence_form.top.wait_window()
		silence_timeout = int(self.my_alarm_silence_form.value)
		print('value got for silence_timeout : alarm popup ' + str(silence_timeout))


def controller():
	'''
	Main function to update reminders list
	and show reminders.
	'''
	global silence_timeout
	silence_timeout = 0
	while(True):
		# usual time.sleep delay is defined at bottom of the loop - for optimizing cpu consumption
		# silence timeout is defined below.
		print('silence_timeout called : ' + str(silence_timeout))
		time.sleep(silence_timeout*60*60)
		silence_timeout=0
		with open(REM_FILE, 'r+') as f:
			entries = json.loads(f.read())

		import datetime
		now = datetime.datetime.now()

		# print('All entries : ' + str(entries.get('reminders')))
		cur_datetime = str(now.strftime("%d-%B-%Y %I:%M:%p")).strip()
		cur_time = str(now.strftime("%I:%M:%p")).strip()
		cur_date = str(now.strftime("%d-%B-%Y")).strip()
		cur_datetime_obj = datetime.datetime.strptime(cur_datetime,'%d-%B-%Y %I:%M:%p')
		cur_time_obj =  datetime.datetime.strptime(cur_time,'%I:%M:%p')
		cur_date_obj =  datetime.datetime.strptime(cur_date,'%d-%B-%Y')
		cur_day_of_month = cur_date.split('-')[0]
		cur_month = cur_date.split('-')[1]

		for reminder in entries.get('reminders').items():
			reminder_datetime_obj = get_datetime_obj_from_str(reminder)
			if cur_datetime_obj >= reminder_datetime_obj:
				print('reminder object to show: ' + str(reminder_datetime_obj))
				# show reminder window
				ShowReminder(reminder)

		for daily_alarm in entries.get('daily_alarms').items():
			snooze_time = daily_alarm[1].get('snooze')
			alarm_time_obj = get_time_obj_from_str(daily_alarm)
			alarm_time_obj = alarm_time_obj + datetime.timedelta(minutes=snooze_time)
			last_execution_date = get_date_obj_from_str(daily_alarm)
			if last_execution_date < cur_date_obj and cur_time_obj >= alarm_time_obj:
				print('daily alarm object to show: ' + str(alarm_time_obj))
				# show reminder window
				ShowAlarm(daily_alarm, 'Daily')

		for weekly_alarm in entries.get('weekly_alarms').items():
			snooze_time = weekly_alarm[1].get('snooze')
			week_alarm_time_obj = get_time_obj_from_str(weekly_alarm)
			week_alarm_time_obj = week_alarm_time_obj + datetime.timedelta(minutes=snooze_time)
			last_execution_date = get_date_obj_from_str(weekly_alarm)
			days_of_week = weekly_alarm[1].get('day_of_week')
			cur_day_of_week = datetime.datetime.today().strftime('%A')[:3]
			if last_execution_date < cur_date_obj and cur_time_obj >= week_alarm_time_obj and cur_day_of_week in days_of_week:
				print('weekly alarm object to show: ' + str(week_alarm_time_obj))
				# show reminder window
				ShowAlarm(weekly_alarm, 'Weekly')
		
		for monthly_alarm in entries.get('monthly_alarms').items():
			snooze_time = monthly_alarm[1].get('snooze')
			month_alarm_time_obj = get_time_obj_from_str(monthly_alarm)
			month_alarm_time_obj = month_alarm_time_obj + datetime.timedelta(minutes=snooze_time)
			last_execution_date = get_date_obj_from_str(monthly_alarm)
			last_execution_month = get_month_from_date(last_execution_date)
			day_of_month_rem = monthly_alarm[1].get('day_of_month')
			if cur_day_of_month >= day_of_month_rem and cur_month != last_execution_month and last_execution_date < cur_date_obj and cur_time_obj >= month_alarm_time_obj:
				print('monthly alarm object to show: ' + str(month_alarm_time_obj))
				# show reminder window
				ShowAlarm(monthly_alarm, 'Monthly')
		
		# delay of 60 seconds
		print('main loop timeout called 10s')
		time.sleep(10)


def get_datetime_obj_from_str(reminder):
	
	import datetime
	reminder_date = str(reminder[1].get('date')).strip()
	reminder_time = str(reminder[1].get('time')).strip()
	reminder_datetime_obj = datetime.datetime.strptime(reminder_date+' '+reminder_time,'%d-%B-%Y %I:%M:%p')
	return reminder_datetime_obj


def get_time_obj_from_str(alarm):
	
	import datetime

	alarm_time = str(alarm[1].get('time')).strip()
	alarm_time_obj = datetime.datetime.strptime(alarm_time,'%I:%M:%p')
	return alarm_time_obj


def get_date_obj_from_str(alarm):
	
	import datetime

	alarm_time = str(alarm[1].get('last_executed')).strip()
	alarm_date_obj = datetime.datetime.strptime(alarm_time,'%d-%B-%Y')
	return alarm_date_obj


def get_month_from_date(alarm_date_obj):
	return alarm_date_obj.strftime("%B")

if __name__ == "__main__":
	controller()