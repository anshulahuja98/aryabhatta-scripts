from robobrowser import RoboBrowser
import tkinter as tk

course_name = []  #A list for storing names of the courses
attendence = []   #A list for storing attendence in those courses

#A class for making GUI more informative and interactive
class Placeholder_State(object):
     __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'with_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):  #To add placeholder in necessary blocks of GUI
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")
    
    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.with_placeholder=True

    def on_focusin(event, entry=entry, state=state):
        if state.with_placeholder:
            entry.delete(0, "end")
            entry.config(fg = state.normal_color, font=state.normal_font)
        
            state.with_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)
            
            state.with_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg = color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")
    
    entry.placeholder_state = state

    return state

def get_data_from(username,password,roll_number):    #A function to do web scrapping
	browser = RoboBrowser()
	# Base URL for all Aryabhatta links
	base_url = "http://172.16.100.161:8080/Aryabhatta_New/"      #Changed the link for new students
	# Attendance report link
	reports = "http://172.16.100.161:8080/Aryabhatta_New/attendanceReport.do"
	# Open login page
	browser.open(base_url)
	form = browser.get_form()
	# Fill login form
	form['userid'].value = username 
	form['password'].value = password
	# Submit form
	browser.submit_form(form)

	# Open main page after login
	browser.open(base_url)

	# Open attendance reports page
	browser.open(reports)

	# Find the course list table 
	table = browser.find_all('table')[1]

	# Get attendance links for all courses
	attendance_links = table.find_all('a', href= re.compile('attendance'))

	# Iterate over attendance links of all courses
	for attendance_link in attendance_links:
		url = base_url + attendance_link['href']
		#print(url)
		browser.open(url)
		# Find the attendance table
		attendance_table = browser.find_all('table')[1]
		# Get all rows from the attendance table
		attendance_rows = attendance_table.find_all('tr')
		# Select the column of roll numbers
		columns = attendance_rows[0]
		# Find the row with same roll numbers as ROLL_NUMBER in personal_row
		personal_row = None
		for attendance_row in attendance_rows :
			if attendance_row.find(text=roll_number):
				personal_row = attendance_row

		# If row for the roll number exists, present the attendance data
		if personal_row is not None:
			lst =[]
			column_data = columns.find_all('td')
			personal_row_data = personal_row.find_all('td')
			course_name.append(browser.find('h3').text)
			for column, personal_data in zip(column_data, personal_row_data):
				if not (browser.find('h3').text == 'Attendance Report for Course OSN1010: Social Connect and Responsibilities - I' or browser.find('h3').text == 'Attendance Report for Course OSN1020: Performing Arts - I'):
					if column.text == 'Total Present in Lecture' or column.text == 'Total Present in Tutorial':      #To take only necessary parts and discard others
						lst.append([column.text+' : '+personal_data.text])	
				else:
					if column.text == 'Total Present in Practical' or column.text == 'Total Number of Practical' :
						lst.append([column.text+' :  '+personal_data.text])		
			attendence.append(lst)
	return course_name,attendence	
def run(username,password,rollno):
	global course_name
	global attendence
	course_name,attendence = get_data_from(username,password,rollno)

Height=500
Width=700


data = {}

count = 0

def get_data():             #Function to handle key pressing in GUI
	global count
	if count<8:
		count+=1
	else:
		count = 0
	name = course_name[count]
	key = name.find(':')
	name = name[key+1:]
	att = attendence[count][0][0]+'\n'+attendence[count][1][0]		
	label_['text'] = name
	label['text'] = att	
			

  #Now creating GUI using TKINTER library
window = tk.Tk()

canvas = tk.Canvas(window,height=Height,width=Width)
canvas.pack()

upper = tk.Frame(window,bg='black', bd=1)
upper.place(relx = 0.5, rely = 0.05,relwidth=0.75,relheight=0.14,anchor='n')

entry_user = tk.Entry(upper,bg = 'lightblue',text='Username',font = ('Times',20))
entry_user.place(relx=0,rely=0,relwidth=0.3,relheight=1)
add_placeholder_to(entry_user, '  Username...')
entry_pass = tk.Entry(upper,bg = 'lightblue',text='password',font = ('Times',20))
entry_pass.place(relx=0.3,rely=0,relwidth=0.3,relheight=1)
add_placeholder_to(entry_pass, '  Password...')
entry_roll = tk.Entry(upper,bg = 'lightblue',text='Rollno.',font = ('Times',20))
entry_roll.place(relx=0.6,rely=0,relwidth=0.3,relheight=1)
add_placeholder_to(entry_roll, '  RollNO...')
button = tk.Button(upper, text = "Login",font = ('Times',15), bg = 'pink',command= lambda: run(entry_user.get(),entry_pass.get(),entry_roll.get()))
button.place(relx=0.9,rely=0,relwidth=0.1,relheight=1)

upper_frame = tk.Frame(window,bg='black', bd=1)
upper_frame.place(relx = 0.5, rely = 0.2,relwidth=0.75,relheight=0.14,anchor='n')

lower_frame = tk.Frame(window, bg = 'black', bd =2)
lower_frame.place(relx = 0.5, rely = 0.35, relwidth=0.75,relheight=0.6,anchor='n')

label = tk.Label(lower_frame,text = 'Fill the details First and then Login'+'\n'+'Press P to get Attendence'+'\n' +'After login button becomes pink again!'+'\n'+'Note: RollNo be like B19CSE090',bg = 'purple',font = ('Times',25),bd=2)
label.place(relx=0,relwidth=1,rely=0,relheight=1)

button = tk.Button(upper_frame,text='P',font = ('Times',25), bg = 'pink',command= lambda: get_data())
button.place(relx=0.92,rely=0,relwidth=0.08,relheight=1)

label_ = tk.Label(upper_frame,text = 'Subject_Name',bg = 'lightblue',font = ('Times',20))
label_.place(relx=0,rely=0,relwidth=0.92,relheight=1)

window.mainloop()

