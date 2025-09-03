#nice little script to run update/upgrade and log the date and time of the success or failure of each into a log file

from datetime import datetime
import subprocess
import sys
import select

#variable holding seconds before the post uu confirmation is skipped
timeout = 5

#funtion controlling the confirm MAGIC
def timed_input(prompt, timeout):
	"""
    Prompts the user for input with a specified timeout.

    Args:
        prompt (str): The message to display to the user.
        timeout (int or float): The number of seconds to wait for input.

    Returns:
        str or None: The user's input string, or None if a timeout occurs.
    """

	print(prompt, end='')# Ensures the prompt is displayed immediately
	sys.stdout.flush()
	# Wait for input on stdin (sys.stdin) for 'timeout' seconds
	ready, _, _ = select.select([sys.stdin], [], [], timeout)
	
	if ready:
		return sys.stdin.readline().strip()
	else:
		return None

#function to run update and confirm the outcome

def update():
	#catch a more accurate date/time
	update_custom_date = datetime.now().strftime("%Y/%m/%d")
	update_custom_time = datetime.now().strftime("%H:%M:%S")
	
	#put the date/time values into a variable 

	update_pass_time = f"Update ran at: {update_custom_time}"
	update_fail_time = f"Update failed at: {update_custom_time}"
	
	#try/except to run update and log the result into file

	try:
		subprocess.run("sudo apt update", shell=True, check=True)
		print("\nUpdate ran correctly!\non: ", update_custom_date, " at: ", update_custom_time, "\n")
		with open(log_file, "a") as file:
			file.write("\n")
			file.write(str(update_pass_time))
	except subprocess.CalledProcessError as e:
		print(f"\nError running update!: {e}\n")
		with open(log_file, "a") as file:
			file.write("\n")
			file.write(str(update_fail_time))
	
	#calling the funtion to provide a time limit for input before continuing automatically		
	timed_input("Press enter key to continue\n", timeout)
	#prints this either way regradless of input or bypass
	print("continuing...\n")
		
#function to run upgrade and confirm the outcome
		
def upgrade():

	#catch accurate date/time

	upgrade_custom_date = datetime.now().strftime("%Y/%m/%d")
	upgrade_custom_time = datetime.now().strftime("%H:%M:%S")
	
	#put date/time into variables

	upgrade_pass_time = f"Upgrade ran at: {upgrade_custom_time}"
	upgrade_fail_time = f"Upgrade failed at: {upgrade_custom_time}"
		
	#try/except to run upgrade and log the result into file
		
	try:
		subprocess.run("sudo apt upgrade", shell=True, check=True)
		print("\nUpgrade ran correctly!\non: ", upgrade_custom_date, " at: ", upgrade_custom_time, "\n")
		with open(log_file, "a") as file:
			file.write("\n")
			file.write(str(upgrade_pass_time))
	except subprocess.CalledProcessError as e:
		print(f"\nError running upgrade!: {e}\n")
		with open(log_file, "a") as file:
			file.write("\n")
			file.write(str(upgrade_fail_time))
			
	timed_input("Press enter key to continue\n", timeout)
	print("continuing...\n")
		
#function for main menu and conditions

def chooseutype():
	choose_loop = True
	choice = ""

	#loop with choices. loop closes if update and upgrade are chosen to do together. otherwise choice to exit has to be selected

	while choose_loop == True:

		choice = input("would you like to update, or upgrade?:\n\n'1': update\n'2': upgrade\n'3': do both\n'4': exit\n")
		
		if choice == "1":
			update()
		elif choice == "2":
			upgrade()
		elif choice == "3":
			update()
			upgrade()
			choose_loop = False
		elif choice == "4":
			print("Exiting application.")
			choose_loop = False
		else:
			print("You've made an invalid choice. Please try again")
			
#define variable to contain the file name

log_file = "uu.txt"
			
#catch the date that the application begins

custom_date = datetime.now().strftime("%Y/%m/%d")

#create variable that'll be converted to string and, append log file to mark session start date

ses_strt_date = f"Session startup date: {custom_date}"
			
with open(log_file, "a") as file:
	file.write(str(ses_strt_date)) 
	
#call the main lobby function
			
chooseutype()

#create variable that'll be converted to string and, append log file with session close time

end_time = datetime.now().strftime("%H:%M:%S")
ses_end_time = f"Session closed at: {end_time}"

#write the session close time to the file

with open(log_file, "a") as file:
	file.write("\n")
	file.write(str(ses_end_time))
	file.write("\n\n\n")
