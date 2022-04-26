#this python code visiting the wp-login page with selenium webdirever(firefox)
#it logins into WordPress dashboard and visits the blog statistics page
#I'm using "Visitor Traffic Real Time Statistics pro" wordpress plugin
#with the power of selenium - bot takes the two screenshots of that plugin page(fullpage and specific-id partial screenshots)
#with the power of tweepy - bot posts predefined message with scraped information(I use beautifulsoup to scrape data for the wordpress analytics page) 
#and attach the 2 screenshots


import platform
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from fake_useragent import UserAgent
import tweepy
from bs4 import BeautifulSoup

#TWITTER API KEYS & TOKENS:
api_key = "#"
api_secrets = "#"
access_token = "#"
access_secret = "#"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)
try:
    api.verify_credentials()
    print("Authentication OK")

except:
    print("Error during authentication")


#WORDPRESS LOGIN PAGE URL(in my case - the url will redirect me to my analytics dashboard after bot submit the data)
bro='https://broplanner.com/wp-admin/admin.php?page=ahc_hits_counter_menu_pro'

#XPATH OF WORDPRESS' LOGIN FORM ELEMENTS
username='//*[@id="user_login"]'
password='//*[@id="user_pass"]'
login_btn='//*[@id="wp-submit"]' #login button xpath, we gonna click on it


#RUN SELENIUM WEBDRIVER
def startbrowser():
    if "Linux" in platform.system():
        path = "geckodriver"
    else:
        path = "geko/geckodriver.exe"
    options = webdriver.FirefoxOptions()
    service = Service(executable_path=path)
    options.add_argument("-disable-dev-shm-usage")
    options.add_argument('-disable-gpu')
    options.add_argument("-no-sandbox")
    options.add_argument("-disable-blink-features=AutomationControlled")
    options.add_argument("-disable-web-security")
    options.add_argument("-disable-xss-auditor")
    useragent = UserAgent().firefox
    print(useragent)
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", useragent)
    driver = webdriver.Firefox(firefox_profile=profile,service=service, keep_alive=False, options=options)
    driver.implicitly_wait(30)
    return driver

#LETS START THE SELENIUM(FIREFOX) BROWSER AND VISIT THE LINKS
#don't forget to change the username and userpassword
def traff(url):
    driver = startbrowser()
    try:
        driver.get(url)
        driver.find_element(by=By.XPATH,value=username).send_keys('username')
        time.sleep(5)
        driver.find_element(by=By.XPATH, value=password).send_keys('userpassword')
        time.sleep(5)
        driver.find_element(by=By.XPATH,value=login_btn).click()
        time.sleep(5)
        #take a fullpage screenshot
        driver.save_full_page_screenshot("fpagescreenshot.png")
        time.sleep(5)
        #take a special element(div) screenshot with selenium webdriver
        driver.find_element(by=By.XPATH,value='//*[@id="wpbody-content"]/div[2]/div[4]/div[2]/div').screenshot('partscreendiv.png')
        time.sleep(5)
    except:
        print("can't run webdriver traff")
        if driver:
            driver.quit()
        pass
    #save the source code for future manipulations with bs4
    source = driver.page_source
    driver.quit()
    
    #CREATING A BEAUTIFULSOUP OBJECT AND PARSE THE HTML
    soup = BeautifulSoup(source, 'html.parser')
    z = soup.find(id="summary_statistics_wrapper")
    td = z.find_all(class_="values")
    #print(td[2].get_text(),td[3].get_text())
    people_amount=td[2].get_text()
    visits=td[3].get_text()
    
    #PREDEFINED TEXT THAT WOULD BE UPLOADED AS A TWEET
    texttt= f"""📈Today's blog analytics: 
Visited by {people_amount} people & had {visits} visits in total

ℹ️☝️this report was created automatically for 🔗broplanner.com
proudly generated with #Python #Selenium #Webdriver #BeautifulSoup and #Tweepy """
    
    #UPLOAD MULTIPLE IMAGES INTO ONE TWEET WITH TWEEPY
    img_names = ['partscreendiv.png', "fpagescreenshot.png"]
    media_ids = []
    for img in img_names:
        xxx = api.media_upload(img)
        media_ids.append(xxx.media_id)
    api.update_status(media_ids=media_ids,status=texttt)
    return "lmao"
x = traff(bro)
