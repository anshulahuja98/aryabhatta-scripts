from robobrowser import RoboBrowser
from dotenv import load_dotenv
import re
import os

# Import and load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Extract environment variables
username =  os.getenv('LDAP')
password =  os.getenv('PASSWORD')
roll_number = os.getenv('ROLL_NUMBER')

# Create browser object
browser = RoboBrowser()
# Base URL for all Aryabhatta links
base_url = "http://172.16.100.161:8080/Aryabhatta/"
# Attendance report link
reports = "http://172.16.100.161:8080/Aryabhatta/attendanceReport.do"
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
	print(url)
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
		print(browser.find('h3').text)
		column_data = columns.find_all('td')
		personal_row_data = personal_row.find_all('td')
		for column, personal_data in zip(column_data, personal_row_data):
			print(column.text,personal_data.text)
