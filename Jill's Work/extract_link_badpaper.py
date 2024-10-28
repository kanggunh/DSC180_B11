import requests
from bs4 import BeautifulSoup
import pandas as pd

#Fetching the webpage content using url
url = 'https://www.nature.com/articles/s41467-019-08507-4'
response = requests.get(url)

# Check if the page is fetched successfully
if response.status_code == 200:
    # Parse the page content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the class where all the reference is stored as a list
    references = soup.find_all('li', class_='c-article-references__item')

    #Initiallized list to store all the URL in the reference
    link_list = []
    for ref in references:
        link = ref.find('a', href=True)
        if link:
            # print(link['href'])
            link_list.append(link['href'])
    
    #Store this result in pandas df
    bad_paperdf = pd.DataFrame({
    "link": link_list,
    "label": 0  # Fill the "label" column with zeros
    })
    #Create a doi row for just the doi in this link column
    bad_paperdf["doi"] = bad_paperdf["link"].apply(lambda x: x.split('doi.org/')[-1] if 'doi.org/' in x else None)



    #Export this pdf as a csv file
    bad_paperdf.to_csv("Jill's Work/bad_paper_link.csv", index=False)

else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
