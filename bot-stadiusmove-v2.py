from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import datetime
from PIL import Image, ImageDraw, ImageFont
import csv
from instagrapi import Client

# --------------------------------------------- Base ---------------------------------------------

chrome_options = webdriver.ChromeOptions()
custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0.2"
chrome_options.add_argument(f"user-agent={custom_user_agent}")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

# --------------------------------------------- Initialize the client ---------------------------------------------

USERNAME = ""
PASSWORD = ""

cl = Client()
cl.login(USERNAME, PASSWORD)

csv_filename = "base.csv"

done = False
new_info = []
need_modif = False
url = "https://www.citeline.fr/info-trafic" # transport company website

# --------------------------------------------- Functions ---------------------------------------------

def image_storie(message):
    image = Image.open( "new_sto.jpg" ) # original model
    d = ImageDraw.Draw(image)
    fnt = ImageFont.truetype("Jost-VariableFont_wght.ttf", 53)
    boucle_largeur = 0
    version_splt = message.split(" ")
    for word in version_splt:
        if boucle_largeur == 0:
            texte_final += word
            boucle_largeur = len(word)
        elif boucle_largeur + len(word) + 1 <= 35:
            texte_final += " " + word
            boucle_largeur += len(word) + 1
        else:
            texte_final += "\n" + word
            boucle_largeur = len(word)
    if len(texte_final) > 530: 
        texte_final = texte_final[:530] + " ..."
    d.text((40,430), texte_final, font=fnt, fill = 'white') # 45 430
    image.save("image_recap.jpg")
    try :
        story = cl.photo_upload_to_story(path="image_recap.jpg")
    except:
        print("Error on a storie")


def read_csv_to_dict_list(csv_filename):
    data = []
    with open(csv_filename, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)
    return data


def save_dict_list_to_csv(info_trafic, csv_filename):
    with open(csv_filename, mode='w') as csv_file: 
        writer = csv.DictWriter(csv_file, fieldnames=["title", "content", "lignes", "link"]) 
        writer.writeheader() 
        writer.writerows(info_trafic)


def find_info(pages) :
    info_trafic = []
    title = ""
    for link in pages :
        try :
            driver.get(link)
            time.sleep(2)
            elements = driver.find_elements('css selector', 'h3.info-traffic-detail-module--title--d711d')

            for element in elements:
                title = element.text

            alt_lignes = ""
            result = []
            elements = driver.find_elements('css selector', 'img.info-traffic-detail-module--linePicto--e39ca')
            for element in elements:
                picto = element.get_attribute('alt')
                alt_lignes += " " + picto

            lignes = ['s01', 'S01', 's02', 'S02', 's03', 'S03', 's04', 'S04', 's05', 'S05', 's06', 'S06', 's07', 'S07', 's08', 'S08', 's09', 'S09', 's10', 'S10', 's11', 'S11', 's12', 'S12', 's13', 'S13', 's14', 'S14', 's15', 'S15', 's16', 'S16', 's17', 'S17', 's18', 'S18', 's19', 'S19', 's20', 'S20', 's21', 'S21', 's22', 'S22', 's23', 'S23', 's24', 'S24', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70']
            for i in lignes :
                if i in alt_lignes :
                    result.append(i.upper())
        except :
            pass
            
        try :
            wait = WebDriverWait(driver, 20)
            content = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div/div[3]')))
            content = content.text
            if "Chers usagers,\n" in content:
                content = content.replace("Chers usagers,\n", "")
            content_split = re.findall(r'\S+|[hH]|\s+', content)
            content_split = [mot.strip() for mot in content_split if mot.strip()] 
            for i in content_split:
                if i in [' s01', ' S01', ' s02', ' S02', ' s03', ' S03', ' s04', ' S04', ' s05', ' S05', ' s06', ' S06', ' s07', ' S07', ' s08', ' S08', ' s09', ' S09', ' s10', ' S10', ' s11', ' S11', ' s12', ' S12', ' s13', ' S13', ' s14', ' S14', ' s15', ' S15', ' s16', ' S16', ' s17', ' S17', ' s18', ' S18', ' s19', ' S19', ' s20', ' S20', ' s21', ' S21', ' s22', ' S22', ' s23', ' S23', ' s24', 's01', 'S01', 's02', 'S02', 's03', 'S03', 's04', 'S04', 's05', 'S05', 's06', 'S06', 's07', 'S07', 's08', 'S08', 's09', 'S09', 's10', 'S10', 's11', 'S11', 's12', 'S12', 's13', 'S13', 's14', 'S14', 's15', 'S15', 's16', 'S16', 's17', 'S17', 's18', 'S18', 's19', 'S19', 's20', 'S20', 's21', 'S21', 's22', 'S22', 's23', 'S23', 's24', 'S24', ' 30', ' 31', ' 32', ' 33', ' 34', ' 35', ' 36', ' 37', ' 38', ' 39', ' 40', ' 41', ' 42', ' 43', ' 44', ' 45', ' 46', ' 47', ' 48', ' 49', ' 50', ' 51', ' 52', ' 53', ' 54', ' 55', ' 56', ' 57', ' 58', ' 59', ' 60', ' 61', ' 62', ' 63', ' 64', ' 65', ' 66', ' 67', ' 68', ' 69', ' 70']:
                    result.append(i.upper())
        except :
            content = ""
        info = {"title": title, "content": content, "lignes": result, "link" : link}
        info_trafic.append(info)
    return info_trafic


def posting_info(info_trafic):
    for info in info_trafic:
        if info['lignes']:
            message = info['title'] + " :\n\nLigne(s) : " + ', '.join(map(str, info['lignes'])) + "\n\n" + info['content']
            image_storie(message)
        else:
            message = info['title'] + " :\n\n" + info['content']
            image_storie(message)

# --------------------------------------------- Main loop ---------------------------------------------

while True:
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    data = read_csv_to_dict_list(csv_filename)

    if 6 <= current_hour < 18:
        try :
            # you can also pass through requests here
            driver.get(url)
            time.sleep(2)
            links = driver.find_elements('css selector', 'a.info-traffic-module--linkNoStyle--89c5a')
            pages = []
            for element in links:
                link = element.get_attribute('href')
                pages.append(link)

            info_trafic = find_info(pages)

            # at least one summary per day
            if not done : 
                lignes_concern = []
                for li in info_trafic :
                    if li["lignes"] :
                        lignes_concern += li["lignes"]
                message_lignes = ""
                first = True
                for i in lignes_concern :
                    if i not in message_lignes and first:
                        message_lignes = str(i)
                        first = False
                    elif i not in message_lignes:
                        message_lignes += ", " + str(i)
                heure = time.ctime().split()
                heure = heure[3]
                message = "Informations trafic du jour : \nActualisation de " + str(heure) + " du " + str(datetime.date.today()) + "\n\n" + message_lignes +"\n\nPlus de précisions ->"
                image_storie(message)

                for info in info_trafic :
                    if info['content'] not in [d['content'] for d in data]:
                        need_modif = True
                posting_info(info_trafic)
                done = True
            else :
                need_modif = False
                for i in info['title'] :
                    if i not in data['title']:
                        need_modif = True
                if need_modif:
                    posting_info(info_trafic)
            if need_modif :
                save_dict_list_to_csv(info_trafic, csv_filename)
                need_modif = False
            
        except :
            print("Loop error !")
        driver.quit()
        current_minute = now.minute
        minutes_until_next_interval = 15 - (current_minute % 15)
        time.sleep(minutes_until_next_interval * 60)
    else:
        minutes_until_next_two_hours = (120 - current_minute) % 120
        done = False
        time.sleep(minutes_until_next_two_hours * 60)
