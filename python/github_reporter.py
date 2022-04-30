#This is Github Code reporter bot
#This is completely raw code, must make exeptions etc etc
#How it works?
#1.Bot using selenium webdriver with gecko to visit the github url(predefined)
#2 It takes the screenshot of the code's body and saves it locally
#3 With power of cv2 library - the screenshot gets divided by height
#4 With power of tweepy library - it done the post to twitter(tweet)
#5 don't forget the predefined attached text for the twitter
# bot dividing the screenshot by 625px and can save unlimited divided-images
# bot will upload only 4 images with twitter's text

import cv2
import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from fake_useragent import UserAgent
import tweepy
from pathlib import Path
img_names=[]
#TWITTER API KEYS & TOKENS:
api_key = ""
api_secrets = ""
access_token = ""
access_secret = ""

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)
try:
    api.verify_credentials()
    print("Authentication OK")

except:
    print("Error during authentication")


#GITHUB PAGE LINK
bro='https://github.com/webprice/pet-projects/blob/main/python/wordpress-analytics-report-to-tweet-twitter.py'

#XPATH OF GITHUB'S CODE BODY
code_place='//*[@id="repo-content-pjax-container"]/div[2]/div/div[4]'



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
def traff(url):
  
#BUT FIRST - REMOVING THE OLD IMG FILES THAT WERE GENERATED BY THIS BOT PREVIOUSLY
    for filename in Path(".").glob("img*.png"):
        filename.unlink()
    driver = startbrowser()
    try:
        driver.get(url)
        time.sleep(15)
        driver.find_element(by=By.XPATH,value='//*[@id="repo-content-pjax-container"]/div/div/div[4]/div[2]/div').screenshot('github.png')
        time.sleep(3)
        driver.quit()
    except:
        print("can't run webdriver traff")
        if driver:
            driver.quit()
        pass
    return "lmao"

  def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

#START THE BOT
x = traff(bro)

#READ THE SCREESHOT WITH CV2 LIBRARY
img = cv2.imread('github.png')
# cv2.imread() -> takes an image as an input
h, w, channels = img.shape

#RESIZE THE ORIGINAL SCREENSHOT IF ITS WIDER 625PX
if w > 625:
    image = image_resize(img, width=625)
    cv2.imwrite('github.png', image)
    img = cv2.imread('github.png')
    # cv2.imread() -> takes an image as an input
    h, w, channels = img.shape
#DIVIDE THE OG SCREENSHOT INTO 625PX PARTS BY HEIGHT
if h > 625:
    divide_number = h // 625
else:
    divide_number = 1
# this is horizontal division
print(h,w)
print(divide_number)
print(range(divide_number))
x=0


#COUNTING HOW MANY PICS WE SHOULD HAVE
#RENDERING THE DIVIDED IMAGES
while x<=divide_number:
    img_name=f'img{x}.png'

    if x == 0:
        img_part = img[:625, :]
        cv2.imwrite(f'img{x}.png', img_part)
        #cv2.imshow('Top', img_part)
        cv2.waitKey(0)
        print("lol")
        x+=1
        img_names.append(img_name)
    if x == divide_number:
        img_part = img[(625 * x):, :]
        cv2.imwrite(f'img{x}.png', img_part)
        #cv2.imshow('Last', img_part)
        cv2.waitKey(0)
        x+=1
        img_names.append(img_name)
    else:
        img_part = img[(x*625):((x+1)*625),:]
        cv2.imwrite(f'img{x}.png', img_part)
        #cv2.imshow(f'Mid{x}', img_part)
        cv2.waitKey(0)
        x+=1
        img_names.append(img_name)


#PREDEFINED TWITTER TEXT FOR A TWEET PURPOSES
texttt = f"""Twitter Automation: "GitHub source code" screenshot maker & divider!
    Bot takes the screenshot of code from a github url, divide it&tweet.

    ℹ️☝️this report was created automatically
    generated with #Python #Selenium #Webdriver #BeautifulSoup #CV2 and #Tweepy """


# UPLOAD MULTIPLE IMAGES INTO ONE TWEET WITH TWEEPY
media_ids = []
media_counter=0
for img in img_names:
    if media_counter>4:
        break
    xxx = api.media_upload(img)
    media_ids.append(xxx.media_id)
    media_counter += 1

api.update_status(media_ids=media_ids, status=texttt)

#LOG TO CONSOLE ALL THE FILES WE HAVE GOT
print(img_names)
#
#