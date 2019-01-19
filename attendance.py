from robobrowser import RoboBrowser
import re
from dotenv import load_dotenv
import os
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

username =  os.getenv('LDAP')
password =  os.getenv('PASSWORD')
roll_number = os.getenv('ROLL_NUMBER')

browser = RoboBrowser()
base_url = "http://172.16.100.161:8080/Aryabhatta/"
reports = "http://172.16.100.161:8080/Aryabhatta/attendanceReport.do"
browser.open(base_url)
form = browser.get_form()
form['userid'].value = username 
form['password'].value = password
browser.submit_form(form)
browser.open(base_url)

browser.open(reports)
table = browser.find_all('table')[1]
attendance_links = table.find_all('a', href= re.compile('attendance'))

for attendance_link in attendance_links:
	url = base_url + attendance_link['href']
	print(url)
	browser.open(url)
	attendance_table = browser.find_all('table')[1]
	attendance_rows = attendance_table.find_all('tr')
	columns = attendance_rows[0]
	personal_row = None
	for attendance_row in attendance_rows :
		if attendance_row.find(text=roll_number):
			personal_row = attendance_row

	if personal_row is not None:
		print(browser.find('h3').text)
		column_data = columns.find_all('td')
		personal_row_data = personal_row.find_all('td')
		for column, personal_data in zip(column_data, personal_row_data):
			print(column.text,personal_data.text)
