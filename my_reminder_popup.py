try:
	# for Python2
	from Tkinter import *
	import tkFont as font
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

		# main frame (inside root) config
		self.mainFrame = Frame(self.root, padx=10, pady = 10, bg="Black")
		self.mainFrame.pack(side="bottom", fill=BOTH, expand=1)

		# reminder label (inside main frame) config
		text = Label(self.mainFrame, text=self.reminder[1].get('reminder'), bg="Black",
					font = font.Font(family="Times", size=18), fg="Orange",
					padx=20, pady=10, wraplength=300)
		date_time_of_trigger = Label(self.mainFrame, text=self.reminder[1].get('date') + " " + self.reminder[1].get('time') , bg="Black",
					font = font.Font(family="Times", size=12), fg="Orange",
					padx=20, pady=10, wraplength=300)
		
		text.pack(fill=BOTH, expand=1)
		date_time_of_trigger.pack(fill=BOTH, expand=1)

		# button frame1 (inside main frame) config
		self.buttonRow = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn1 = Button(self.buttonRow, text="Dismiss", command=self.dismissReminder, fg="Orange", bg="Black").grid(row=0, column=0)
		self.btn2 = Button(self.buttonRow, text="Edit", command=self.editReminder, fg="Orange", bg="Black").grid(row=0, column=3)
		self.buttonRow.grid_columnconfigure(3, minsize=10)
		self.buttonRow.pack()
		
		# button frame2 (inside main frame) config
		self.buttonRow2 = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn3 = Button(self.buttonRow2, text="Remind in 10", command=self.remindIn10, fg="Orange", bg="Black").grid(row=0, column=1)
		self.btn4 = Button(self.buttonRow2, text="Remind in an hour", command=self.remindInHour, fg="Orange", bg="Black").grid(row=0, column=2)
		self.btn5 = Button(self.buttonRow2, text="Remind me T'moro", command=self.remindTomorrow, fg="Orange", bg="Black").grid(row=0, column=3)
		self.buttonRow2.grid_columnconfigure(3, minsize=10)
		self.buttonRow2.pack()
		
		# button frame3 (inside main frame) config
		self.buttonRow3 = Frame(self.mainFrame, padx=10, pady=10, bg="Black")
		self.btn6 = Button(self.buttonRow3, text="Remind in a Week", command=self.remindInWeek, fg="Orange", bg="Black").grid(row=0, column=1)
		self.btn7 = Button(self.buttonRow3, text="Remind in a Month", command=self.remindInMonth, fg="Orange", bg="Black").grid(row=0, column=2)
		self.btn8 = Button(self.buttonRow3, text="Remind in 3 Months", command=self.remind3Months, fg="Orange", bg="Black").grid(row=0, column=3)
		self.buttonRow3.grid_columnconfigure(3, minsize=10)
		self.buttonRow3.pack()

		self.root.lift()
		self.root.attributes("-topmost", True)
		self.root.bind('<Control-d>', lambda event: self.dismissReminder())

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


	def dismissReminder(self):
		'''
		utitlity function to remove reminder form list
		'''
		# move the active reminder to completed ones
		with open(REM_FILE, 'r+') as f:
			reminders = json.loads(f.read())
			x = reminders.get('reminders').pop(self.reminder[0])
			print('completed : ' + str(x))
			reminders.get('completed_reminders').update({self.reminder[0]:x})

		# write the updated values
		with open(REM_FILE, 'w') as f:
			f.write(json.dumps(reminders))

		self.root.destroy()
		print('destroy called\n')


	def postpone_for(self, time_in_mins):
		'''
		utility function to postpone reminder by 10 minutes
		'''
		
		import datetime
		with open(REM_FILE, 'r+') as f:
			reminders = json.loads(f.read())
			print('reminders before postpone : ' + str(reminders))
			x = reminders.get('reminders').get(self.reminder[0])
			reminder_obj = (str(self.reminder[0]),x)
			print('reminder to be postponed :' + str(reminder_obj))
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
			print('reminders after postpone : ' + str(reminders))
		
		#write back updated time for the reminder
		with open(REM_FILE, 'w') as f:
			f.write(json.dumps(reminders))

		self.root.destroy()
		print('destroy called\n')
		
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


	def remindTomorrow(self):
		'''
		utility function to postpone reminder by 1 day
		'''
		self.postpone_for(60*24)


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
		self.root.destroy()
		print('self.reminder : ' + str(self.reminder))
		my_reminder_create_form.Reminder(self.reminder)


def controller():
	'''
	Main function to update reminders list
	and show reminders.
	'''
	while(True):

		with open(REM_FILE, 'r+') as f:
			entries = json.loads(f.read())

		import datetime
		now = datetime.datetime.now()

		print('All entries : ' + str(entries.get('reminders')))
		cur_datetime = str(now.strftime("%d-%B-%Y %I:%M:%p")).strip()
		cur_datetime_obj = datetime.datetime.strptime(cur_datetime,'%d-%B-%Y %I:%M:%p')

		for reminder in entries.get('reminders').items():

			reminder_datetime_obj = get_datetime_obj_from_str(reminder)

			print('reminder date time object ' + str(reminder_datetime_obj))
			print('curremt date time object ' + str(cur_datetime_obj))
			if cur_datetime_obj >= reminder_datetime_obj:
				print('reminder to show: ' + str(reminder_datetime_obj))
				# show reminder window
				ShowReminder(reminder)

		# for alarms in entries.get('alarms').items():

		# 	print('alarm time object ' + str(reminder_datetime_obj))
		# 	print('curremt time object ' + str(cur_datetime_obj))
		# 	if cur_time_obj >= alarm_time_obj:
		# 		print('alarm to show: ' + str(reminder_datetime_obj))
		# 		# show reminder window
		# 		ShowReminder(reminder)
		
		# delay of 60 seconds	
		time.sleep(10)

def get_datetime_obj_from_str(reminder):
	
	import datetime

	reminder_date = str(reminder[1].get('date')).strip()
	# print('reminder date : ' + str(reminder_date))
	reminder_time = str(reminder[1].get('time')).strip()
	# print('reminder_time : ' + reminder_time)
	reminder_datetime_obj = datetime.datetime.strptime(reminder_date+' '+reminder_time,'%d-%B-%Y %I:%M:%p')
	return reminder_datetime_obj


if __name__ == "__main__":
	controller()