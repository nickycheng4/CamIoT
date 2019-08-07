import pyautogui 
import socket
import time

def video_control(dec, counter):
	print(pyautogui.size()) 
	print(pyautogui.position()) 

	# counter = 1

	print(dec)
	if dec =='':
		return

	if dec == 'Middle':
		pyautogui.press('space')
	elif dec == 'Left':
		counter -= 1
		if counter < 0:
			counter = 0
		pyautogui.press(str(counter))
	elif dec == 'Right':
		counter += 1
		if counter > 9:
			counter = 9
		pyautogui.press(str(counter))
	else:
		pyautogui.press('esc')

	return counter
	# pyautogui.moveTo(1920/2, 1080/2)
		
		# skype control
		# if dec == 'Y' or 'y':
		# 	pyautogui.click(1920-80, 1080-50) 
		# else:
		# 	# pyautogui.moveTo(100, 100, duration = 1)
		# 	pyautogui.click(1920-30, 1080-100) 

		# pyautogui.moveTo(1920/2, 1080/2, duration = 1)


		# # Slides Control
		# # dec = input('your choise (up/dn/hm): ')
		# if dec == 'up':
		# 	pyautogui.press('up')
		# elif dec == 'dn':
		# 	pyautogui.press('down') 
		# else:
		# 	pyautogui.press('home') 

		# # Music Control
		# # dec = input('your choise (play/stop/up/dn): ')
		# if dec == 'play' or 'stop':
		# 	pyautogui.click(1920/2, 1080/2) 
		# elif dec == 'up':
		# 	pyautogui.click(1920/2, 1080/2) 
		# else:
		# 	pyautogui.click(1920/2, 1080/2) 

# pyautogui.hotkey("ctrlleft", "a")
# for i in range(10):
# 	pyautogui.press('down')
# for i in range(10):
# 	pyautogui.press('up')
# pyautogui.typewrite(["a", "left", "ctrlleft"]) 











































