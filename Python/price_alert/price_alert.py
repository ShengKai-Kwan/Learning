from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import os
import datetime

"""
This application purposely for price monitoring and alerting. 
with using the Rakuten trade platform (Malaysia) to collect real-time data 
and Whatsapp for alerting the user.

"""

url = "https://www.rakutentrade.my/login/"
#usrname = ""                            # set your rakuten username
#psswd = ""                              # set your rakuten password
symbols = [                             # [[{symbol}, {minTpAlert}, {maxTpAlert}, {eachBidValue}, 0], [{symbol2}, {minTpAlert2}, {maxTpAlert2}, {eachBidValue}, 0], []...]
    ['istone', 0.16, 0.175, 0.005, 0],
    ['binacom', 0.425, 0.455, 0.005, 0]
]
refreshTime = 47                        # The application will collect data every {refreshTime} seconds, reserves 13 seconds for system process time. refreshTime + 13 seconds = 60seconds.
load_time = 4                           # Loading time, to wait the browser load the page. Increase the load_time if you have poor/slow internet connection, else decrease
whatsapTarget = ""                      # The target name. Replace with your friend or group name. For myself, i created a new group to send the alert message.


chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument('--disable-gpu')
driver = webdriver.Chrome ("chromedriver.exe",options=chrome_opt)    # ensure the chromedriver.exe in the same directory with spammer.py
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

def searchSymbol(whatsappTab):

    for symbol in symbols:
        print("Opening new Tab for: "+ symbol[0] + "...")
        driver.execute_script("window.open('about:blank', '" + symbol[0] + "');")
        driver.switch_to.window(symbol[0])
        driver.get (url)
        # search for the symbol
        time.sleep(load_time+4)
        print("Entering Symbol: " + symbol[0] + "...")
        driver.find_element_by_css_selector("input.search-input.scene-input.ui-input-text.ui-body-a").send_keys(symbol[0])
        time.sleep (load_time)
        print("Searching Symbol: " + symbol[0] + "...")
        driver.find_element_by_css_selector("ul.symbol_list_ul").click()


        # Inform user : Initiating Monitoring on {symbol}
        time.sleep(load_time+1)
        print('Monitoring :' + symbol[0].upper())
        try:
            alert("Monitoring Symbol: " + symbol[0].upper(), whatsappTab)
        except Exception as e:
            print(e)
            print("Check Whatsapp Connection!")

def monitorSymbol(whatsappTab):
    currentDT = datetime.datetime.now ()
    log = currentDT.strftime("%I:%M:%S %p").ljust (15, " ")

    for symbol in symbols:
        # monitor
        driver.switch_to.window (symbol[0])
        time.sleep (load_time)
        driver.find_element_by_css_selector ("div.refresh.date-and-time").click ()

        price = driver.find_element_by_css_selector ("span.last").text
        dtime = driver.find_element_by_css_selector ("div.time-date-val").text[14:]
        volume = driver.find_element_by_css_selector ("div.info-blk.vol > div.val").text
        volume_string_len = len (volume) - 1
        if volume[volume_string_len] == "M":
            volume = int (float (volume[0:volume_string_len - 1]) * 1000000)
        else:
            volume = int (volume.replace (",", ""))
        volume = int (volume)
        volume_dif = volume - symbol[4] # symbol[3] is last volume recorded, volume difference = current total volume - last recorded volume
        symbol[4] = volume # update latest volume
        log = log + "|" + str(price).ljust(10, ' ') + "|" + str(format(int(volume_dif), ',')).ljust(10, ' ')
        if float (price) >= symbol[2]:
            alert (
                "{symbol};Max Target Price: {maxTp};Total Volume: {volume};Current Price: {price};Vol. Chg.: {volume_dif};{dtime}".format (
                    symbol=symbol[0].upper (), maxTp=symbol[2], volume=format (volume, ','), price=price,
                    volume_dif=format (volume_dif, ','), dtime=dtime), whatsappTab)
            symbol[2] = symbol[2] + symbol[3]

        if float (price) <= symbol[1]:
            alert (
                "{symbol};Min Target Price: {minTp};Total Volume: {volume};Current Price: {price};Vol. Chg.: {volume_dif};{dtime}".format (
                    symbol=symbol[0].upper (), minTp=symbol[1], volume=format (volume, ','), price=price,
                    volume_dif=format (volume_dif, ','), dtime=dtime), whatsappTab)
            symbol[1] = symbol[1] - symbol[3]

    print(log + "|")

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


    input("Press enter to continue AFTER YOU LOGGED IN TO Rakuten...")

    """
    # log in
    time.sleep(load_time)
    print("Entering Username...")
    driver.find_element_by_id ("loginName").send_keys (usrname)
    print("Entering Password...")
    driver.find_element_by_id ("password").send_keys(psswd)
    print("Logging in...")
    driver.find_element_by_id ('login-btn').click()
    """
    searchSymbol (whatsappTab)
    os.system('CLS')

    header = ' '.center(15, ' ')
    header2 = 'Time'.center(15, ' ')
    for symbol in symbols:
        header = header + '|' + symbol[0].center(21)
        header2 = header2 + "|" + "Price".center(10, " ")+ "|" + "Vol. Chg.".center(10, " ")

    print(header + "|")
    print(header2 + "|")

    while True:
        monitorSymbol(whatsappTab)
        time.sleep (refreshTime)  # stop for {refreshTime}} seconds


try:
    main()
except Exception as e:
    print(e)
    driver.quit()
except KeyboardInterrupt:
    print('\nQuitting....')
    driver.quit()
    exit()
finally:
    driver.quit()
    ('\nExiting program....')
    exit()