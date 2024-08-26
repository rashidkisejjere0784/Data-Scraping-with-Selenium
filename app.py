import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
 
# create webdriver object
driver = webdriver.Firefox()
# get google.co.in
page = 34
driver.get(f"https://nation.africa/service/search/kenya/290754?pageNum={page}&query=%22Huduma%20Namba%22&sortByDate=true")

df = pd.DataFrame()
contents = []
headers = []
dates = []

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

    index = 0
    length = 7

    while True:  # Loop to handle stale element reference
        try:
            # Re-fetch the article collection after each navigation
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "article-collection"))
            )

            # Find all articles
            articles = element.find_elements(By.TAG_NAME, "li")
            print(len(articles), index)
            if len(articles) != length:
                driver.back()
                continue

            while index < len(articles):
                article = articles[index]
                header = article.find_element(By.TAG_NAME, "h3")
                date = article.find_element(By.CLASS_NAME, "date").text

                if len(contents) == len(headers):
                    headers.append(header.text)
                    dates.append(date)
                
                try:
                    # Click the article header to navigate to the article page
                    header.click()

                    # Wait for the content block to load
                    content = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "article-page"))
                    )

                    # Print the content text
                    # Append the content to the dataframe
                    contents.append(content.text)
                    index += 1
                    driver.back()
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "article-collection"))
                    )
                
                except ElementClickInterceptedException as e:
                    pass

                except Exception as e:
                    pass

            break  # Exit the loop if successful
        
        except StaleElementReferenceException:
            print("Stale element reference encountered. Retrying...")
            continue  # Retry the loop if a stale element reference is encountered

        except ElementClickInterceptedException as e:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tibrr-cookie-consent-button"))
            )
            cookie_button.click()
            continue

finally:
    driver.quit()

df['Header'] = headers
df['Date'] = dates
df['Content'] = contents
name = "3"
df.to_excel(f'articles_{name}_{page}.xlsx', index=False)
try:
    main = pd.read_excel(f"articles_{name}.xlsx")
except:
    main = pd.DataFrame(columns=df.columns)

combined = pd.concat([main, df], axis=0)

combined.to_excel(f"articles_{name}.xlsx", index=False)