"""This python file is basically loading in 2 dataframe that store link to the research paper and extract the text for classifications."""
import pandas as pd
import numpy as np
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from enum import Enum
import re
from urllib.error import URLError, HTTPError  # Import these classes from urllib.error
import ssl

def get_text(soup):
    #Given a beautiful soup object, it will extact the text
    for script in soup(['script', 'style']):
        script.extract()
    text = soup.get_text(separator=' ')
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def create_txt_list(df, col_name):
    #Function that given dataframe and column name that stores the link, 
    #We will extract the text and store them into a list
    #This function returns a modified df where they add a new column "text" associated with an list. 
    text_lst = []
    page_count = 0
    for link in df[col_name]:
        page_count += 1
        print(f"Analyzing {page_count}th link")
        try:
            page = urlopen(link)
            print("Page accessed successfully.")
        except HTTPError as e:
            print(f"HTTP error occurred: {e.code} - {e.reason}")
            if e.code == 403 and e.reason == 'Forbidden':
                print("Found a forbidden access exception ")
                hdr = {'User-Agent': 'Mozilla/5.0'}
                try:
                    # Retrying with modified request headers
                    request = Request(link, headers=hdr)
                    page = urlopen(request)
                    print("Page accessed successfully with headers.")
                except HTTPError as retry_e:
                    print(f"Retry HTTP error occurred: {retry_e.code} - {retry_e.reason}")
                    text_lst.append("HTTP Error, No Access")
                    continue
                except URLError as retry_e:
                    print(f"Retry URL error occurred: {retry_e.reason}")
                    text_lst.append("URL Error, No Access")
                    continue
            else:
                print("NOT a forbidden access exception ")
                text_lst.append("HTTP Error, No Access")
                continue
        except URLError as e:
            print(f"URL error occurred: {e.reason}")
            text_lst.append("URL Error, No Access")
            continue
        except ssl.SSLError as e:
            print(f"SSL error occurred: {e}")
            text_lst.append("SSL Error, No Access")
            continue
        except ValueError as e:
            print(f"Value error (likely an invalid URL): {e}")
            text_lst.append("Invalid URL No Access")
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            text_lst.append("Unexpected Error No Access")
            continue
        html_content = page.read().decode("utf-8")
        soup = BeautifulSoup(html_content, "html.parser")
        text_lst.append(get_text(soup))
        print()
    df['text'] = text_lst
    return df


# Read in the csv file
## This is a csv file that teammates manually inspected as good research pape
good_df = pd.read_csv("150 Research paper.csv")[['Link']]
good_df['label'] = 1

## This is a csv file that generated from extract_link_badpaper.py
bad_df = pd.read_csv("Irrelevent_paper.csv")
bad_df['label'] = 0

#Extract text from good text dataframe
bad_df_text = create_txt_list(bad_df, "link")
#Extract text from good dataframe
good_df_text = create_txt_list(good_df, "Link")

##All the paper that couldn't accessed is stored as specific value in the column to be filtered out
pass_bad_df = bad_df_text[(bad_df_text['text'] != "HTTP Error, No Access") & (bad_df_text['text'] != "Redirecting")]
pass_good_df = good_df_text[(good_df_text['text'] != "HTTP Error, No Access") & (good_df_text['text'] != "Redirecting")]
pass_good_df = pass_good_df.rename(columns={'Link': 'link'})

#Combine these two dataframe and export them to be used for various classification. 
merged_df = pass_good_df.append(pass_bad_df, ignore_index=True)
merged_df.to_csv('merged_label.csv', index=False)