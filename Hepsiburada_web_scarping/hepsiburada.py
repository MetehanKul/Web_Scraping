from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/114.0.0.0"
}

a = 1
product_list = []


while a <= 50:
    time.sleep(5)
    r = requests.get(f"https://www.hepsiburada.com/ara?q=gamer%20notebook&sayfa={a}" , headers= headers)
    soup = BeautifulSoup(r.content , "html.parser")

    st1 = soup.find("div" , attrs={"class" : "productListContent-tEA_8hfkPU5pDSjuFdKG"})
    st2 = st1.find("ul" , attrs={"class" : "productListContent-frGrtf5XrVXRwJ05HUfU productListContent-rEYj2_8SETJUeqNhyzSm"})
    st3 = st2.find_all("li" , attrs={"class" : "productListContent-zAP0Y5msy8OHn5z7T_K_"})
    

    for i in st3:
        link_end = i.a.get("href")
        link_start = "https://www.hepsiburada.com"
        link = link_start + link_end
        print(link)
        try:   
            time.sleep(1)
            r1 = requests.get(link , headers=headers)
            sp1 = BeautifulSoup(r1.content , "html.parser")

            Title = sp1.find("div" , attrs={"class" : "raeVnaSg0g9mMFTxKLRf"}).text.strip()
            Price = sp1.find("div" , attrs= {"class" : "rNEcFrF82c7bJGqQHxht"}).text.strip()
            Rating = sp1.find("div" , attrs= {"class" : "JHvKSZxdcgryD4RxfgqS"}).text.strip()
            Salesman = sp1.find("a" , attrs= {"class" : "W5OUPzvBGtzo9IdLz4Li"}).text.strip()
            Evaluation = sp1.find("a" , attrs= {"class" : "yPPu6UogPlaotjhx1Qki"}).text.strip()
            Brand =  sp1.find("a" , attrs = {"data-test-id" : "brand"}).text.strip()


            features_raw = sp1.find_all("div", attrs={"class": "OXP5AzPvafgN_i3y6wGp"})
            features = [feature.get_text(strip=True) for feature in features_raw]

            values_raw = sp1.find_all("div", attrs={"class": "AxM3TmSghcDRH1F871Vh"})
            values = [value.get_text(strip=True) for value in values_raw]

            feature_dict = dict(zip(features, values))

            feature_dict["Title"] = Title
            feature_dict["Salesman"] = Salesman
            feature_dict["Price"] = Price
            feature_dict["Evaluation"] = Evaluation
            feature_dict["Brand"] = Brand

            product_list.append(feature_dict)
        except:
            feature_dict = {
                    "Title": np.nan,
                    "Salesman": np.nan,
                    "Price": np.nan,
                    "Evaluation": np.nan,
                    "Brand": np.nan
                }
            product_list.append(feature_dict)
            
        selected_features = [
                'Title', 'Brand' ,'Salesman', 'Ekran Kartı', 'SSD Kapasitesi', 'Ram Tipi',
                'Ram (Sistem Belleği)','İşlemci Nesli', 'İşlemci Tipi', 'Evaluation', 
                'Price']
    
    a+=1

df = pd.DataFrame(product_list)

df = df[selected_features]
df.columns =  ['Title', 'Brand', 'Salesman', 'Graphics Card', 'SSD Capacity', 'RAM Type', 'RAM', 'Processor Generation', 'Processor Type', 'Evaluation', 'Price']
df.dropna(how = "all" , inplace = True)
df.to_excel("hepsiburada.xlsx" , index=False)