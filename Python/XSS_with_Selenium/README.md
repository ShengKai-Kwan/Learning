# Simple Mail Merge

A tool that search for "\<input\>" element, attempt to inject payload that has potential vulnerable to XSS (stored and reflected).

#### Requirement
This tool requires several modules:
- Selenium

##### Install Module
```pip
pip install selenium
```
#### Features
1. Search for \<input\> Element with attribute "Type" of Text and Password
2. Inject xss payload 
3. Identify either payload run successful 

#### Usage
```
    Bot = BotXss(r"chromedriver", "https://www.hackthissite.org/")
```

Initiating BotXss with two parameters
1. param1 : path to your suitable chrome driver
2. param2 : targeted  url



#### Update notes
9 OCT 2020 : Created project - XSS_with_selenium 
