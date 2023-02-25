import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import unquote
from tqdm import tqdm
import time


# Crawing all the grid links for 5 pages
o = "https://www.amazon.in/s?i=apparel&bbn=1968024031&rh=n%3A1571271031%2Cn%3A1968024031%2Cn%3A1968120031%2Cp_89%3AAdidas&dc&ds=v1%3As5L%2B%2BjYgWw0tO9G%2BZ1TtXmMYAnckXV7U2x2R2KZ5qz4&qid=1677156605&rnid=1968024031&ref=sr_nr_n_1"
number_of_pages = 5
grid_link_url = []
for i in range(number_of_pages):
    if i == 0:
        grid_link_url.append(o)
    else:
        split = o.split("&qid")
        p = split[0] + "&page={}&qid".format(i) + split[1]
        print(i,split[0])
        grid_link_url.append(p)
    
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

#collecting all the Product Links from the above grid link
# grid_page = "a"
link = []
for grid_url in tqdm(grid_link_url):
    grid_page = requests.get(grid_url,headers=headers)
    print(grid_page)

    grid_page_soup = BeautifulSoup(grid_page.content,"html.parser")
    grid_page_soup1 = BeautifulSoup(grid_page_soup.prettify(),"html.parser")

    elements = grid_page_soup1.find_all(class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")

   
    for element in elements:
        # print(element.get("href"))
        x = element.get("href")
        x = unquote(x.split("&url=")[-1])
        x = "https://www.amazon.in"+x
        
        link.append(x)

#scraping title,number_of_rating,brand,price,star_rating from the collected link
title,number_of_rating,brand,price,star_rating,link1 = [],[],[],[],[],[]
for links in tqdm(link):
    url = links
    #print(links)
    page = requests.get(url,headers=headers)
    link1.append(links)

    # if page == "Response [200]":
    soup = BeautifulSoup(page.content,  "html.parser")
    soup1 = BeautifulSoup(soup.prettify(),'html.parser')



    try:
        title.append(soup1.find(id="productTitle").get_text().strip())
    #title.strip()
    except:
        title.append("null")
        print(links,"title")
    try:
        number_of_rating1 = soup1.find(id="acrCustomerReviewText").get_text().strip()
        number_of_rating1 = re.sub(r'\D', '', number_of_rating1)
        number_of_rating.append(number_of_rating1)
    except:
        number_of_rating.append("null")
        print(links,"number_of_rating")
    try:    
        brand.append(soup1.find(id="bylineInfo").get_text().strip())
    
    except:
        brand.append("null")
        print(links,"brand")
    
    try:
        price.append(soup1.find(class_="a-price-whole").get_text().strip().replace(",",""))    
    except:
       price.append("null")
       print(links,"price")
    
    try:
        star_rating.append(soup1.find(class_="a-icon-alt").get_text().strip().replace("out of 5 stars",""))
    except:
        star_rating.append("null")
        print(links,"star rating")    

    time.sleep(10)

#creating a dataframe
zip = list(zip(title,number_of_rating,brand,star_rating,link1))
df = pd.DataFrame(zip,columns=["Product Name","Number of Rating","Brand","Star Rating","Links"])
df.to_csv("test.csv")

# data cleaning
def replacing(to_be_cleaned):
    cleaning_words = ["Visit the ","Store","Brand",":"]
    
    for word in cleaning_words:
        to_be_cleaned = to_be_cleaned.replace(word,"")
    return to_be_cleaned

df["Brand"].apply(replacing)

#saving
df.to_csv("test.csv")