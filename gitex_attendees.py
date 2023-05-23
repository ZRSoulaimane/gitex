from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import openpyxl

chromeDriverLocation = "chromedriver"
attendees = list()

def get_chromedriver(chromeDriverLocation, use_proxy=False, user_agent=None):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--user-agent=%s' % user_agent)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")

    return webdriver.Chrome(executable_path=chromeDriverLocation, options=chrome_options)

def get_links(driver, page_number):
    driver.get(f"https://gitexafrica.expoplatform.com/newfront/participants?page=delegates&limit=60&pageNumber={page_number}")

    links = []
    wait = WebDriverWait(driver, 20)

    try:
        link_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, f'//*[@id="__next"]/div[2]/div[1]/main/div/div/div[3]/div[2]/div/div[1]/*//a')))

        links = [link.get_attribute("href") for link in link_elements]
    except:
        print("Links not found")
        return None

    return links
def execute_att(file_names, loop_starts, loop_ends):
    driver = get_chromedriver(chromeDriverLocation)
    driver.get(f"https://gitexafrica.expoplatform.com/newfront/participants?page=delegates&limit=60&pageNumber={1}")
    time.sleep(10)
    # wait = WebDriverWait(driver, 15)
    # number_of_pages = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[3]/div[2]/div/div[2]/nav/ul/li[last()-1]'))).text
    all_links = []

    sign_in_button_homepage = driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[2]/div[2]/div/button')
    sign_in_button_homepage.click()


    # Fill in the email and password fields
    email_input = driver.find_element(By.XPATH, '//*[@id="username"]')
    email_input.send_keys("mbouchiha@gear9.ma")
    password_input = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_input.send_keys("$Gitex2023")

    # Click on the sign-in button in the modal
    sign_in_button_modal = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div/div[2]/form/button')
    sign_in_button_modal.click()
    # Wait for the sign-in process to complete

    for page_number in range(loop_starts, loop_ends):
        links = get_links(driver, page_number)
        print("number_of_pages : "+str(page_number))
        if links is None:
            break
        all_links.extend(links)

    attendees = []
    print(all_links)

    # Define the list of keys
    keys = [
        "nom",
        "position",
        "entreprise",
        "web_site",
        "linkedin",
        "COUNTRY OF RESIDENCE",
        "CATEGORY",
        "COMPANY TYPE",
        "COMPANY INDUSTRY",
        "COMPANY INDUSTRY - SUB - TECHNOLOGY",
        "PRODUCTS & SERVICES (INTEREST)"
        # Add more keys here
    ]

    # df_empty = pd.DataFrame(columns=keys)

    
    for link in list(set(all_links)):
        time.sleep(7)
        attendee = {}
        driver.get(link)
        time.sleep(5)
        # wait = WebDriverWait(driver, 30)

        name_xpath_options = [
            '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[2]/div[2]/div/div/div[1]/div/div[3]/h2',
            '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[2]/div[2]/div/div/div/div/div[3]/h2'
        ]
        name = ''
        for xpath in name_xpath_options:
            try:
                # name = wait.until(EC.visibility_of_element_located((By.XPATH, xpath))).text
                name = driver.find_element(By.XPATH, xpath).text
                # print("name", name)
                break
            except:
                print("Element name not found")
                pass

        position_xpath_options = [
            '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[2]/div[2]/div/div/div[1]/div/div[4]/p[1]',
            '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[2]/div[2]/div/div/div/div/div[4]/p[1]'
        ]
        position = ''
        for xpath in position_xpath_options:
            try:
                # position = wait.until(EC.visibility_of_element_located((By.XPATH, xpath))).text
                position = driver.find_element(By.XPATH, xpath).text
                break
            except:
                print("Element position not found")
                pass

        entreprise_xpath_options = [
            '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[2]/div[2]/div/div/div[1]/div/div[4]/p[2]',
            '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[2]/div[2]/div/div/div/div/div[4]/p[2]'
        ]
        entreprise = ''
        for xpath in entreprise_xpath_options:
            try:
                # entreprise = wait.until(EC.visibility_of_element_located((By.XPATH, xpath))).text
                entreprise = driver.find_element(By.XPATH, xpath).text
                break
            except:
                print("Element entreprise not found")
                pass

        web_site_xpath_options = [
            '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/a/h6',
            '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/a/h6'
        ]
        web_site = ''
        for xpath in web_site_xpath_options:
            try:
                # web_site = wait.until(EC.visibility_of_element_located((By.XPATH, xpath))).text
                web_site = driver.find_element(By.XPATH, xpath).text
                break
            except:
                print("Element web_site not found")
                pass

        linkedin_xpath_options = [
            '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/a',
            '//*[@id="__next"]/div[2]/div[1]/main/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[2]/a'
        ]
        linkedin = ''
        for xpath in linkedin_xpath_options:
            try:
                # linkedin_element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                linkedin_element =  driver.find_element(By.XPATH, xpath)
                linkedin = linkedin_element.get_attribute("href")
                break
            except:
                print("Element linkdin not found")
                pass
            
        # Assign the fetched values to the attendee dictionary
        attendee["nom"] = name
        attendee["position"] = position
        attendee["entreprise"] = entreprise
        attendee["web_site"] = web_site
        attendee["linkedin"] = linkedin

        data = {
        'COUNTRY OF RESIDENCE': '',
        'CATEGORY': '',
        'COMPANY TYPE': '',
        'COMPANY INDUSTRY': '',
        'COMPANY INDUSTRY - SUB - TECHNOLOGY': '',
        'PRODUCTS & SERVICES (INTEREST)': ''
        }

        try:
            # card = wait.until(EC.visibility_of_element_located((By.ID, "matchmaking_info")))
            card = driver.find_element(By.ID, "matchmaking_info")
            elements = card.find_elements(By.XPATH, ".//div/div")
            for element in elements:
                key_element = element.find_element(By.XPATH, ".//span")
                key = key_element.text
                try:
                    value_element = element.find_element(By.XPATH, ".//p")
                    value = value_element.text
                except :
                    value = ''
                data[key] = value
        except :
            # Handle the case where the card is not found
            pass

        consolidated_data = {**attendee, **data}
        attendees.append(consolidated_data)
        print(attendees)
        
    df = pd.DataFrame(attendees)

    # df.to_excel("GITEX2023.xlsx",sheet_name="attendees")  

    df.to_csv(file_names)

    driver.quit()