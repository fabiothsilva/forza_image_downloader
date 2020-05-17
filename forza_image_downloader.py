import os
from time import sleep
from getpass import getpass
import pprint

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

# Variables to store the user email and password
# For the password uses the getpass method, so
# the caracters are not displayed while typping
user = input('Enter the email of your Microsoft account:\n')

pwd = getpass('Enter the password of your Microsoft account:\n')

# Creates a selenium browser object
browser = webdriver.Firefox()

# I have a two monitor setup, so I move the browser window
# to the second monitor. Change the values to move the window
# to a different location or comment the line below to ignore it
browser.set_window_position(-1000,0)

# Opens the browser on the Forza motosport gallery webpage
# Assuming that you are not loggedin, a login page will be displayed
# After the login, we will be redirected to the Forza gallery
browser.get('https://forzamotorsport.net/gallery')

# Locates the login field
user_elem = browser.find_element_by_css_selector("input[name='loginfmt'][type='email']")

# Fills the login field with the user email
user_elem.send_keys(user)

# Locates the next button
next_elem = browser.find_element_by_id("idSIButton9")

# Clicks on the next button
next_elem.click()

# Locates the password field.
# Since the webpage can take some time to load the password field
# We wait for 2 seconds or until the element apears,whatever happens first
pwd_ele = WebDriverWait(browser,2).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='passwd'][type='password']")))

# Fills the password elemente with the user password.
pwd_ele.send_keys(pwd)

# Locates the login button
log_elem = browser.find_element_by_id("idSIButton9")

# Click the login button
log_elem.click()

# Once logged in, you will be redirected to your gallery
# Keep in mind that I only have pictures of Forza Horizon 4 and
# something around 30 pictures, so I dont know if the page displayed will be the same
# if you have pictures of other Forza games, or if after a certain quantity of pictures
# a new page is created. Let me know if you have any issues with that

# Locates the pictures elements.
# Since the webpage can take some time to load the pictures
# We wait for 60 seconds or until the element apears,whatever happens first
# This will return a list with all the pictures web elements.
photo_links = WebDriverWait(browser,60).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a[class='clearfix']")))

# Creates a new folder to store the pictucres that will be downloaded
# Change to path to your desired folder

root_folder = r"PATH/TO/THE/DESIRED/FOLDER"

os.makedirs(os.path.join(root_folder,"Forza_Dowloads"),exist_ok = True)

# Variable to store the full path of the new folder
folder = os.path.join(root_folder,"Forza_Dowloads")

print (f"{len(photo_links)} photos found.\n")

print ("Downloading photos...\n")

# A for loop to iterate over each photo web element
# For each picture, we extract the direct link to the image file
# And save that file in the Forza_Downloads folder
# The iterator is decorated by tqdm to show a progress bar
for index,link in enumerate(tqdm(photo_links,desc="Progress", unit="photo", ncols=150)):
    index += 1

    url = link.get_attribute('href')

    r = requests.get(url)

    r.raise_for_status()

    with open (os.path.join(folder,(str(index)+".jpeg")),"wb") as image:
        for chunk in r.iter_content(100000):
            image.write(chunk)

print(f"\nImages saved to {folder}\n")

# After the download of all your pictures, we will log you out

# Locates the logout button
logout_elem = browser.find_element_by_css_selector("a[class='signout']")

# Clicks the logout button
logout_elem.click()

# Closes the browser
browser.close()

# Now we will resize the photos for a more suitable Instagram landscape resolution
# Because some shoots are too much beautiful to stay in your hard drive
print("Optimizing photos for Instagram...\n")

# Creates a folder named Insta_Resize inside the Forza_Dowloads folder
os.makedirs(os.path.join(folder,"Insta_Resize"),exist_ok=True)

dir_files = []
# A for loop that iterates over each file in the Forza_Downloads folder
# and append only the files into dir_files, excluding the recently created folder
# This is necessary just to not cause a malfunction with the tqdm progress bar
# when resizing the images
for file in os.listdir(folder):
    if file.endswith('.jpeg'):
        dir_files.append(file)

# A for loop that iterates over each file in the Forza_Downloads folder
# Each jpeg file will be resized to the resolution 1080x566
# Then the file will be ranamed to n_1080_566.jpeg
# and saved in the folder Insta_Resize
for file in tqdm(dir_files,desc="Progress",total=len(photo_links), unit="resized photo", ncols=150):
    if file.endswith(".jpeg"):
        img_obj = Image.open(os.path.join(folder,file))
        file_name, ext = os.path.splitext(file)
        resized_img = img_obj.resize((1080,566))        
        resized_img.save(os.path.join(folder,"Insta_Resize",(file_name + "_1080_566.jpeg")))
   