from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass

print('#############################################\n')

username = str(raw_input('Enter your email address or UserName: '))
passwd = getpass.getpass()#str(input('Enter current Password: '))
new_passwd = getpass.getpass()#str(input('Enter New password: '))


driver = webdriver.Firefox();
driver.get("http://m.facebook.com")
try:
	assert 'Welcome' in driver.title
except:
	print('->User Already logged in!\n Do you want to logout? [Y/N]')
	ch = raw_input()
	while(True):
		if ch == 'Y':
			driver.find_element_by_partial_link_text('Logout').click()
			print('Restart this program and try again!')
			exit(0)
		elif ch == 'N':
			print('Thank you for using the script.')
			exit(0)
		else:
			print("Invalid Choice, try again [Y/N]")

email = driver.find_element_by_name('email')
email.clear()
email.send_keys(username)
pascode = driver.find_element_by_name('pass')
pascode.send_keys(passwd)
driver.find_element_by_name('login').click()

try:
	assert 'New! Easier Login' not in driver.page_source
except:
	driver.get('http://m.facebook.com/login/save-device/cancel/')

try:
	#assert 'The email address or phone number' in driver.get_page_source()
	#assert "The password that you've entered" in driver.get_page_source()
	#assert "It looks like you entered a slight misspelling" in driver.get_page_source()
	assert (driver.title == "Facebook")
except:
	print('Wrong email or password... Restart please\n########################')
	exit(0)

def success():
	print("#####################")
	print("Old Password: " + passwd)
	print("New Password: " + new_passwd)
	print("Logged Out Successfully :)")
	print("#####################")
	driver.close()
	

def changePassword():
	driver.find_element_by_link_text('Settings & Privacy').click()
	driver.find_element_by_link_text('General').click()
	driver.find_element_by_link_text('Password').click()
	driver.find_element_by_name('old_password').send_keys(passwd)
	driver.find_element_by_name('new_password').send_keys(new_passwd)
	driver.find_element_by_name('confirm_password').send_keys(new_passwd)
	driver.find_element_by_name('save').click()
	try:
		assert 'You cannot use this password.' not in driver.page_source
	except:
		changePassword()
	driver.find_element_by_name('session_invalidation_options').click()
	driver.find_element_by_name('submit_action').click()
	try:
		driver.find_element_by_partial_link_text('Logout').click()
	except:
		driver.find_element_by_partial_link_text('Log Out').click()
	with open("Log.txt", "a") as fil:
		#fil.write("##########\nOld Passed: "+passwd+"\n New Password: "+new_passwd+"\n#############################\n")
		print "Success"
	success()
	exit(0)


changePassword()
	








#
