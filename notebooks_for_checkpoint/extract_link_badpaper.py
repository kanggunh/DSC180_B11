"""Run this python file to create a dataframe of all irrelevent papers in perovskite research"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# Initialize WebDriver (e.g., Chrome)
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome()
url_2 = 'https://www.sciencedirect.com/science/article/pii/S2590238524001711'

# Open the research paper URLz
driver.get(url_2)

# Locate the references section (adjust as needed)
references = driver.find_elements(By.XPATH, "//ol[@class='references']//a[contains(@class, 'anchor anchor-primary')]")
# references = driver.find_elements_by_xpath("//a[@class='anchor anchor-primary']")

# Extract and print the links
# link_list = [ref.get_attribute('href') for ref in references if ref.get_attribute('href')]
link_list = [ref.get_attribute('href') for ref in references if ref.get_attribute('href')]


print("Extracted links:", link_list)

# Close the driver
driver.quit()

#Fetching the webpage content using url
url_1 = 'https://www.nature.com/articles/s41467-019-08507-4'
response_1 = requests.get(url_1)

# Check if the page is fetched successfully
if response_1.status_code == 200:
    # Parse the page content using Beautiful Soup
    soup = BeautifulSoup(response_1.content, 'html.parser')

    # Find the class where all the reference is stored as a list
    references = soup.find_all('li', class_='c-article-references__item')

    #Initiallized list to store all the URL in the reference
    for ref in references:
        link = ref.find('a', href=True)
        if link:
            # print(link['href'])
            link_list.append(link['href'])
    

else:
    print(f"Failed to fetch the page. Status code: {response_1.status_code}")

link_set = set(link_list)
link_list_unique = list(link_set)
#Store this result in pandas df
bad_paperdf = pd.DataFrame({
"link": link_list_unique
})

#Comment this code because now link_list is not just doi link, but any link in general!!
# #Create a doi row for just the doi in this link column
# bad_paperdf["doi"] = bad_paperdf["link"].apply(lambda x: x.split('doi.org/')[-1] if 'doi.org/' in x else None)

#Export this pdf as a csv file
bad_paperdf.to_csv("../Irrelevent_paper.csv", index=False)

'''
DO THIS ONCE link_list is completed!!!
    #Store this result in pandas df
    bad_paperdf = pd.DataFrame({
    "link": link_list
    # ,"label": 0  # Fill the "label" column with zeros
    })
    #Create a doi row for just the doi in this link column
    bad_paperdf["doi"] = bad_paperdf["link"].apply(lambda x: x.split('doi.org/')[-1] if 'doi.org/' in x else None)



    #Export this pdf as a csv file
    bad_paperdf.to_csv("Jill's Work/bad_paper_big.csv", index=False)
    '''
