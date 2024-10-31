import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    link_list = []
    for ref in references:
        link = ref.find('a', href=True)
        if link:
            # print(link['href'])
            link_list.append(link['href'])
    

else:
    print(f"Failed to fetch the page. Status code: {response_1.status_code}")

url_2 = 'https://www.sciencedirect.com/science/article/pii/S2590238524001711'
response_2 = requests.get(url_2)

if response_2.status_code == 200:
    #Parse
    soup = BeautifulSoup(response_2.content, 'html.parser')
    references = soup.find_all('li', class_='references')
    print(references)

    for ref in references:
        link = ref.find('a', href = True)
        if link:
            link_list.append(link['href'])

else:
    print(f"Failed to fetch second page. Status code: {response_2.status_code}")

print(link_list)

#Store this result in pandas df
bad_paperdf = pd.DataFrame({
"link": link_list
})
#Create a doi row for just the doi in this link column
bad_paperdf["doi"] = bad_paperdf["link"].apply(lambda x: x.split('doi.org/')[-1] if 'doi.org/' in x else None)

#Export this pdf as a csv file
bad_paperdf.to_csv("Irrelevent_paper", index=False)

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
