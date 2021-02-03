from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import urllib.request
from email.mime.multipart import MIMEMultipart
import smtplib
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import schedule
from time import sleep
import fake_useragent



attempt = True
mod1 = ""
mod2 = ""
img1 = ""
img2 = ""
mod1_discr = ""
mod2_discr = ""
textfilepath = r"path to -> content.txt"
directory = "path to -> imgs/{}"
#Clear the text file
g = open(textfilepath, "r+")
g.truncate(0)


def email(title1, title2, message1, message2):


    FROM = "from"


    msg = MIMEMultipart("related")
    msg["From"] = FROM
    msg["To"] = "to"
    msg['Date'] = formatdate(localtime=True)
    msg["Subject"] = "Banshee Mods"
    msg.preamble = f"---------------------\nMESSAGE WAS SEND WITH PYTHON\n\n\nMessage"

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    msgText = MIMEText(f'---------------------\nMESSAGE WAS SEND WITH PYTHON\n\n\nMessage')
    msgAlternative.attach(msgText)

    msgText = MIMEText(f'<b>{message1}</b><br><img src="cid:image1"><br><b>{message2}</b><br><img src="cid:image2">', 'html')
    msgAlternative.attach(msgText)
    f1 = open(f'imgs/{title1}.jpg' , 'rb')
    msgImage1 = MIMEImage(f1.read())
    msgImage1.add_header('Content-ID', '<image1>')
    msg.attach(msgImage1)
    f1 = open(f'imgs/{title2}.jpg' , 'rb')
    msgImage1 = MIMEImage(f1.read())
    msgImage1.add_header('Content-ID', '<image2>')
    msg.attach(msgImage1)

    #load in the password for the email address
    with open(r'path to -> password.txt' , "r") as f:
        password = f.read()

    #"25" is the port for smtp
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.connect("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login(FROM, password)
    server.sendmail(FROM, msg["To"], msg.as_string())



#Downloads image if not already available with proper filename
def download_img(file1, file2, file1_url, file2_url, direc=directory):
    file1_url = file1_url
    file2_url = file2_url

    urllib.request.urlretrieve(file1_url, direc.format(f"{file1}.jpg"))
    urllib.request.urlretrieve(file2_url, direc.format(f"{file2}.jpg"))


def get_mods():
    global attempt
    global mod1
    global mod2
    global img1
    global img2
    global mod1_discr
    global mod2_discr

    ua = fake_useragent.UserAgent(fallback='Chrome')
    user_agent = ua.data_randomize[2]
    url = "https://www.todayindestiny.com/vendors"
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1,1")
    options.add_argument("user-agent="+user_agent)
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)



    #Waiting for page to load
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "vendorCardContainer")))
        attempt = True
    except TimeoutException:
        g = open(textfilepath , "w+")
        g.write("Page timed out after 20 secs.")
        g.close()
        attempt = False



    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    #"filter" the page source to be only banshee
    page = soup.find_all("div", {"hash":"672118013"})

    for p in page:
        # finds the images to the Mods
        # maybe needs to be changed when Banshee's amount of Mods/items changes
        img1 = p.find_all("img", class_="inventoryItemIcon")[7]["src"]
        img2 = p.find_all("img", class_="inventoryItemIcon")[8]["src"]
        
        # Write url of imgs into "content.txt"
        # Somehow img1 may not work the way intended
        g = open(textfilepath , "w+")
        g.write("\nIMG1: "+img1)
        g.write("\nIMG2: "+img2)
        g.close()

        #MOD 1
        mod1_name = p.find_all("p", class_="itemTooltip_itemName")[15]
        mod1_type = p.find_all("p", class_="itemTooltip_itemType")[15]
        #Getting Text from inbetween the tags
        mod1_name = str(mod1_name).split('<p class="itemTooltip_itemName">')
        mod1_name = mod1_name[1].split('</p>')
        mod1_type = str(mod1_type).split('<p class="itemTooltip_itemType">')
        mod1_type = mod1_type[1].split('</p>')

        mod1_discr = mod1_name[0]+" : "+mod1_type[0]

        mod1 = mod1_name[0] +" "+ mod1_type[0]


        #MOD 2
        mod2_name = p.find_all("p", class_="itemTooltip_itemName")[17]
        mod2_type = p.find_all("p", class_="itemTooltip_itemType")[17]
        #Getting Text from inbetween the tags
        mod2_name = str(mod2_name).split('<p class="itemTooltip_itemName">')
        mod2_name = mod2_name[1].split('</p>')
        mod2_type = str(mod2_type).split('<p class="itemTooltip_itemType">')
        mod2_type = mod2_type[1].split('</p>')

        mod2_discr = mod2_name[0]+" : "+mod2_type[0]

        mod2 = mod2_name[0] +" "+ mod2_type[0]
        
        # Writes Mod name into content.txt
        g = open(textfilepath , "w+")
        g.write("\nMOD1: "+mod1)
        g.write("\nMOD2: "+mod2)
        g.close()


    #keeps the program running until the driver has no timeout
    if attempt == True:
        attempt = True
    elif attempt == False:
        attempt = False


#runs the whole script
def execute():
    global mod2_discr
    global mod1_discr
    get_mods()
    while 1:
        if attempt == True:
            break
        elif attempt == False:
            get_mods()


    mod1_url = img1
    mod2_url = img2
    filename1 = mod1
    filename2 = mod2

    try:
        email(filename1, filename2, mod1_discr, mod2_discr)
    except:
        download_img(filename1, filename2, mod1_url, mod2_url)
        email(filename1, filename2, mod1_discr, mod2_discr)


execute()

##Scheduling script
#schedule.every().day.at("19:05").do(execute)
#
#while 1:
#    schedule.run_pending()
#    sleep(1)
