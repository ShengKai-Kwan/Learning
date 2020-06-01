from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import html
import time
import sys

"""
This application purposely for price monitoring and alerting. with using the Rakuten trade platform (Malaysia) to collect real-time data and Whatsapp for alerting the user.

"""

driver = webdriver.Chrome ("chromedriver_83.exe")   # ensure the chromedriver.exe in the same directory with price_alert.py
                                                    # ensure the chromedriver.exe match the your chrome browser's version
url = "https://www.rakutentrade.my/login/"
usrname = "" #set your rakuten username
psswd = "" # set your rakuten password
symbol = "krono" # set the symbol you wish to monitor
maxTpAlert = 0.51 # when real-time price larger or equal maxTpAlert, the application will trigger an alert
minTpAlert = 0.5 # when real-time price smaller or equal minTpAlert, the application will trigger an alert
refreshTime = 60 # The application will collect data every {refreshTime} seconds
load_time = 5 # Loading time, to wait the browser load the page. Increase the load_time if you have poor/slow internet connection, else decrease
whatsapTarget = "Testing" # The target name. Replace with your friend or group name. For myself, i created a new group to send the alert message.

def alert(msg):
    driver.switch_to.window (whatsappTab)
    child_elem = driver.find_element_by_xpath ("//span[@title='" + whatsapTarget + "']")
    parent_elem = child_elem.find_element_by_xpath ('./../../../../..')
    parent_elem.click ()
    time.sleep (load_time)

    inputField = driver.find_element_by_css_selector ('div._3F6QL._2WovP')
    msgs = msg.split(';')
    inputField.send_keys (msgs[0])
    for i in range(1,len(msgs)):
        action = ActionChains (driver)
        action.key_down (Keys.SHIFT)
        action.send_keys (Keys.ENTER)
        action.key_up (Keys.SHIFT)
        action.perform ()
        inputField.send_keys(msgs[i])
        #inputField.send_keys(msgs[i].encode('utf-8'))

    driver.find_element_by_css_selector ("button._35EW6").click()
    driver.switch_to.window ("rakutenTab")

# open web whatsapp
driver.get ("https://web.whatsapp.com/")
whatsappTab = driver.window_handles[0]
input("Press enter to continue AFTER YOU LOGGED IN TO WHATSAPP...")

# open url
driver.execute_script("window.open('about:blank', 'rakutenTab');")
driver.switch_to.window("rakutenTab")
driver.get (url)

# log in
time.sleep(load_time)
print("Entering Username...")
driver.find_element_by_id ("loginName").send_keys (usrname)
print("Entering Password...")
driver.find_element_by_id ("password").send_keys(psswd)
print("Logging in...")
driver.find_element_by_id ('login-btn').click()


# search for the symbol
time.sleep(load_time+2)
print("Entering Symbol...")
driver.find_element_by_css_selector("input.search-input.scene-input.ui-input-text.ui-body-a").send_keys(symbol)
time.sleep (load_time)
print("Searching Symbol...")
driver.find_element_by_css_selector("ul.symbol_list_ul").click()


# get latest details of the symbol
time.sleep(load_time+1)
try:
    print("Initiating Monitoring... sending message through whatsapp...")
    #alert("Monitoring Symbol: " + symbol.upper())
except Exception as e:
    print("Check Whatsapp Connection!")

time.sleep (load_time)
while True:
    price = driver.find_element_by_css_selector ("span.last").text
    dtime = driver.find_element_by_css_selector ("div.time-date-val").text
    print (dtime + ', RM: ' + price)
    if (float(price) >= 0.165):#maxTpAlert

        alert("{symbol};Max Target Price: {maxTp};Current Price: {price};{dtime}".format (symbol=symbol.upper (),maxTp=maxTpAlert, price=price,dtime=dtime))

    if (float(price) <= minTpAlert):
        alert ("{symbol};Max Target Price: {minTp};Current Price: {price};{dtime}".format (symbol=symbol.upper (),
                                                                                           minTp=minTpAlert, price=price,
                                                                                           dtime=dtime))

    time.sleep (refreshTime)  # stop for 30 seconds
    driver.find_element_by_css_selector ("div.refresh.date-and-time").click()
