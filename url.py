import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
 
# create webdriver object
driver = webdriver.Chrome()
# get google.co.in
page =13
driver.get(f"https://nation.africa/service/search/kenya/290754?pageNum={page}&query=eCitizen&sortByDate=true")

df = pd.DataFrame()
links = []
headers = []


try:
    # Wait for and click the cookie consent button
    cookie_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tibrr-cookie-consent-button"))
    )
    cookie_button.click()
    
    # Wait for the article collection to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "article-collection"))
    )

    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "article-collection"))
    )

    # Find all articles
    articles = element.find_elements(By.TAG_NAME, "li")

    for article in articles:
        header = article.find_element(By.TAG_NAME, "h3")
        a_tag = article.find_element(By.TAG_NAME, "a")
        link = a_tag.get_attribute("href")

        # Append the header and link to the respective lists
        headers.append(header.text)
        links.append(link)

except Exception as e:
    pass
                

df['Header'] = headers
df['urls'] = links

main = pd.read_csv("urls.csv")

# Merge the two dataframes

df = pd.concat([main, df], axis=0)

df.to_csv("urls.csv", index=False)