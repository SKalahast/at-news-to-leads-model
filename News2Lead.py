import pandas as pd
from selenium.webdriver.common.keys import Keys
from newspaper import Article
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import dateparser

options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
chromeOptions.add_argument("--no-sandbox") 
chromeOptions.add_argument("--disable-setuid-sandbox") 
chromeOptions.add_argument("--remote-debugging-port=9222")  # this
chromeOptions.add_argument("--disable-dev-shm-using") 
chromeOptions.add_argument("--disable-extensions") 
chromeOptions.add_argument("--disable-gpu") 
chromeOptions.add_argument("start-maximized") 
chromeOptions.add_argument("disable-infobars")


all_client_df = pd.read_csv('DSC_Company_List.csv')

def news_2_leads(client,start_date,end_date):
    
    title=[]
    Texts=[]
    all_links = []
    date_item = []
    company_name = []
    url = 'https://www.google.com/'
    
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    # driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    driver.quit()
    
    driver.get(url)
    try:
        driver.find_element(By.XPATH,"//*[text()='Stay signed out']").click()
    except:
        pass
    # try:          
    g_search = driver.find_element(By.XPATH,"//*[@title='Search']")       
    g_search.send_keys(client +" news, -stock")
    g_search.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.refresh()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[text()='News']").click()
    time.sleep(2)
    driver.refresh()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[text()='Tools']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[@class='KTBKoe']").click()
    time.sleep(2)
    driver.switch_to.active_element
    driver.find_element(By.XPATH,"//*[text()='Custom range...']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[@class='T3kYXe']/input[8]").send_keys(start_date)
    time.sleep(1)
    driver.find_element(By.XPATH,"//*[@class='T3kYXe']/input[9]").send_keys(end_date)
    time.sleep(1)
    driver.find_element(By.XPATH,"//*[text()='Go']").click()
    
    time.sleep(3)

    while True:
        try:
            news_results = driver.find_elements(By.XPATH,"//*[@class='WlydOe']")
            
            for news_div in news_results:
                try:
                    company_name.append(client)
                    news_link = news_div.get_attribute('href')
                    all_links.append(news_link)
                except:
                    all_links.append("Link not captured")
            
            time.sleep(2)       
            news_date = driver.find_elements(By.XPATH,"//*[@class='OSrXXb rbYSKb LfVVr']")
            for elem in news_date:
                try:
                    item = elem.text
                    date = dateparser.parse(item)
                    date_item.append(date.strftime("%Y-%m-%d"))
                except:
                    date_item.append("Date not captured")
            time.sleep(2)
                # print(date_item)        
            try:
                driver.find_element(By.XPATH,"//*[text()='Next']").click()
                time.sleep(2)
            except:
                break
        except NoSuchElementException:
            pass
                
    count = 0  
    my_count = 0
    for data in tqdm(all_links):
        
        try:
            article=Article(data)    
            article.download()
            article.parse()
            t = article.title
            txt=article.text
    
            title.append(t)
            Texts.append(txt)
            count += 1
        except:
            print('Check parsing')
            print(count)
            title.append('not found')
            Texts.append('not found')
    
        print('TESTING')
       
        my_count +=1        
    # except NoSuchElementException:
    #     pass
    df = pd.DataFrame({'News_Date':date_item, 'Account_Name':company_name,'Headline':title, 'Content':Texts,'URL':all_links})
    if df.empty:
        pass
    else:
        df = df[(df["Headline"].str.contains('not found')==False)]
        df = df[(df["News_Date"].str.contains('Date not captured')==False)]
        df = df[(df["URL"].str.contains("Link not captured")==False)]
    
    driver.quit()
    return df

def all_clients(start_date,end_date):
    
    title=[]
    Texts=[]
    all_links = []
    date_item = []
    company_name = []
    url = 'https://www.google.com/'
    
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    # driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    driver.quit()
    
    for client in all_client_df['Client Name']:
        driver.get(url)
        try:
            driver.find_element(By.XPATH,"//*[text()='Stay signed out']").click()
        except:
            pass
        try:         
            g_search = driver.find_element(By.XPATH,"//*[@title='Search']")       
            g_search.send_keys(client +" news, -stock")
            g_search.send_keys(Keys.ENTER)
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.XPATH,"//*[text()='News']").click()
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.XPATH,"//*[text()='Tools']").click()
            time.sleep(2)
            driver.find_element(By.XPATH,"//*[@class='KTBKoe']").click()
            time.sleep(2)
            driver.switch_to.active_element
            driver.find_element(By.XPATH,"//*[text()='Custom range...']").click()
            time.sleep(2)
            driver.find_element(By.XPATH,"//*[@class='T3kYXe']/input[8]").send_keys(start_date)
            time.sleep(1)
            driver.find_element(By.XPATH,"//*[@class='T3kYXe']/input[9]").send_keys(end_date)
            time.sleep(1)
            driver.find_element(By.XPATH,"//*[text()='Go']").click()
            
            time.sleep(2)
            while True:
                try:
                    news_results = driver.find_elements(By.XPATH,"//*[@class='WlydOe']")
                    
                    for news_div in news_results:
                        try:
                            company_name.append(client)
                            news_link = news_div.get_attribute('href')
                            all_links.append(news_link)
                        except:
                            all_links.append("Link not captured")
                    
                    time.sleep(2)       
                    news_date = driver.find_elements(By.XPATH,"//*[@class='OSrXXb rbYSKb LfVVr']")
                    for elem in news_date:
                        try:
                            item = elem.text
                            date = dateparser.parse(item)
                            date_item.append(date.strftime("%Y-%m-%d"))
                        except:
                            date_item.append("Date not captured")
                    time.sleep(2)
                        # print(date_item)        
                    try:
                        driver.find_element(By.XPATH,"//*[text()='Next']").click()
                        time.sleep(2)
                    except:
                        break
                except NoSuchElementException:
                    pass
            driver.refresh()
        except StaleElementReferenceException:
            pass
        driver.refresh()
    count = 0  
    my_count = 0
    for data in tqdm(all_links):
        article=Article(data)    
        article.download()
        try:
            article.parse()
            t = article.title
            txt=article.text
    
            title.append(t)
            Texts.append(txt)
            count += 1
        except:
            print('Check parsing')
            print(count)
            title.append('not found')
            Texts.append('not found')
    
        print('TESTING')
       
        my_count +=1        
       
    df = pd.DataFrame({'News_Date':date_item, 'Account_Name':company_name,'Headline':title, 'Content':Texts,'URL':all_links})
    if df.empty:
        pass
    else:
        df = df[(df["Headline"].str.contains('not found')==False)]
        df = df[(df["News_Date"].str.contains('Date not captured')==False)]
        df = df[(df["URL"].str.contains("Link not captured")==False)]
    
    driver.quit()
    return df


def multi_clients(client,start_date,end_date):
    
    title=[]
    Texts=[]
    all_links = []
    date_item = []
    company_name = []
    url = 'https://www.google.com/'
    
    driver = webdriver.Chrome(options=options)
    
    for client_name in client:
        driver.get(url)
        try:
            driver.find_element(By.XPATH,"//*[text()='Stay signed out']").click()
        except:
            pass
        try:         
            g_search = driver.find_element(By.XPATH,"//*[@title='Search']")       
            g_search.send_keys(client_name +" news, -stock")
            g_search.send_keys(Keys.ENTER)
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.XPATH,"//*[text()='News']").click()
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.XPATH,"//*[text()='Tools']").click()
            time.sleep(2)
            driver.find_element(By.XPATH,"//*[@class='KTBKoe']").click()
            time.sleep(2)
            driver.switch_to.active_element
            driver.find_element(By.XPATH,"//*[text()='Custom range...']").click()
            time.sleep(2)
            driver.find_element(By.XPATH,"//*[@class='T3kYXe']/input[8]").send_keys(start_date)
            time.sleep(1)
            driver.find_element(By.XPATH,"//*[@class='T3kYXe']/input[9]").send_keys(end_date)
            time.sleep(1)
            driver.find_element(By.XPATH,"//*[text()='Go']").click()
            
            time.sleep(2)
            while True:
                try:
                    news_results = driver.find_elements(By.XPATH,"//*[@class='WlydOe']")
                    
                    for news_div in news_results:
                        try:
                            company_name.append(client_name)
                            news_link = news_div.get_attribute('href')
                            all_links.append(news_link)
                        except:
                            all_links.append("Link not captured")
                    
                    time.sleep(1)       
                    news_date = driver.find_elements(By.XPATH,"//*[@class='OSrXXb rbYSKb LfVVr']")
                    for elem in news_date:
                        try:
                            item = elem.text
                            date = dateparser.parse(item)
                            date_item.append(date.strftime("%Y-%m-%d"))
                        except:
                            date_item.append("Date not captured")
                    time.sleep(1)
                        # print(date_item)        
                    try:
                        driver.find_element(By.XPATH,"//*[text()='Next']").click()
                        time.sleep(1)
                    except:
                        break
                except NoSuchElementException:
                    pass
            driver.refresh()
        except StaleElementReferenceException:
            pass
        driver.refresh()
    count = 0  
    my_count = 0
    for data in tqdm(all_links):
        article=Article(data)    
        article.download()
        try:
            article.parse()
            t = article.title
            txt=article.text
    
            title.append(t)
            Texts.append(txt)
            count += 1
        except:
            print('Check parsing')
            print(count)
            title.append('not found')
            Texts.append('not found')
    
        print('TESTING')
       
        my_count +=1        
       
    df = pd.DataFrame({'News_Date':date_item, 'Account_Name':company_name,'Headline':title, 'Content':Texts,'URL':all_links})
    if df.empty:
        pass
    else:
        df = df[(df["Headline"].str.contains('not found')==False)]
        df = df[(df["News_Date"].str.contains('Date not captured')==False)]
        df = df[(df["URL"].str.contains("Link not captured")==False)]
    
    driver.quit()
    return df
      



