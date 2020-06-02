from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import html
import time
import sys
import os

"""
This application purposely for price monitoring and alerting. with using the Rakuten trade platform (Malaysia) to collect real-time data and Whatsapp for alerting the user.

"""

url = "https://www.rakutentrade.my/login/"
usrname = ""        # set your rakuten username
psswd = ""         # set your rakuten password
symbol = ""           # set the symbol you wish to monitor
maxTpAlert = 0.17           # when real-time price larger or equal maxTpAlert, the application will trigger an alert
minTpAlert = 0.16           # when real-time price smaller or equal minTpAlert, the application will trigger an alert
refreshTime = 60            # The application will collect data every {refreshTime} seconds
load_time = 6               # Loading time, to wait the browser load the page. Increase the load_time if you have poor/slow internet connection, else decrease
whatsapTarget = ""   # The target name. Replace with your friend or group name. For myself, i created a new group to send the alert message.
last_volume = 0             # initial volume always 0


chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument('--disable-gpu')
driver = webdriver.Chrome ("chromedriver_83.exe",options=chrome_opt)    # ensure the chromedriver.exe in the same directory with price_alert.py
                                                                        # ensure the chromedriver.exe match the your chrome browser's version
def alert(msg, whatsappTab):
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

    driver.find_element_by_css_selector ("button._35EW6").click()
    driver.switch_to.window ("rakutenTab")

def main():
    os.system('CLS')
    # open web whatsapp
    driver.get ("https://web.whatsapp.com/")
    whatsappTab = driver.window_handles[0]
    input("Press enter to continue AFTER YOU LOGGED IN TO WHATSAPP...")

    # open url
    print("Opening Rakutentrade.my")
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
        os.system('CLS')
        print("Initiating Monitoring... ")
        alert("Monitoring Symbol: " + symbol.upper(), whatsappTab)
    except Exception as e:
        print("Check Whatsapp Connection!")

    time.sleep (load_time)
    while True:
        price = driver.find_element_by_css_selector ("span.last").text
        dtime = driver.find_element_by_css_selector ("div.time-date-val").text
        volume = driver.find_element_by_css_selector ("div.info-blk.vol->div.val").text
        volume_dif = volume - last_volume
        last_volume = volume
        print (dtime + ', Total Volume: ' + volume + ', RM: ' + price + ', Volume: ' + volume_dif)
        if float(price) >= maxTpAlert:

            alert("{symbol};Max Target Price: {maxTp};Current Price: {price};{dtime}".format (symbol=symbol.upper (),
                                                                                               maxTp=maxTpAlert, volume=volume, price=price, volume_dif=volume_dif,
                                                                                               dtime=dtime), whatsappTab)

        if float(price) <= minTpAlert:
            alert ("{symbol};Min Target Price: {minTp};Total Volume: {volume};Current Price: {price};Volume: {volume_dif};{dtime}".format (symbol=symbol.upper (),
                                                                                               minTp=minTpAlert, volume=volume, price=price, volume_dif=volume_dif,
                                                                                               dtime=dtime), whatsappTab)

        time.sleep (refreshTime)  # stop for {refreshTime}} seconds
        driver.find_element_by_css_selector ("div.refresh.date-and-time").click()

try:
    main()
except Exception as e:
    print(e)
    driver.quit()
except KeyboardInterrupt:
    print('\nQuitting....')
    driver.quit()
    exit()