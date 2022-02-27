

from selenium import webdriver
import time 
import csv
import json


product_title = []
product_image_url = []
product_price= []
product_details= []



import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="username",
  password="password",
  database="databasename"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE data_table (product_title VARCHAR(255), product_price VARCHAR(255), product_image_url VARCHAR(500), product_details VARCHAR(1000))")

with open('file_path/Amazon Scraping - Sheet1.csv', newline='') as f_input:
    csv_input = csv.DictReader(f_input)
    i=0
    list=[]
    for row in csv_input:     
      if i<150:
       country=row['country']
       asin=row['Asin']
       page=f"https://www.amazon.{country}/dp/{asin}"
       list.append(page)
       i+=1
start_time = time.time()       
for link in list:
  chrome_driver_path="/Users/pc/Downloads/Compressed/chromedriver"

  driver=webdriver.Chrome(executable_path=chrome_driver_path)

  driver.get(link)
  try:
      title=driver.find_element_by_id("productTitle")    
      product_title.append(title.text)
      details=driver.find_element_by_class_name("a-expander-content")
      product_details.append(details.text)
      image_url=driver.find_element_by_tag_name("img").get_attribute("src")
      product_image_url.append(image_url)
      price=driver.find_element_by_class_name("a-color-price")   
      product_price.append(price.text)
      sql = "INSERT INTO data_table (product_title, product_price, product_details, product_image_url) VALUES (%s, %s, %s, %s)"
      val = (title.text, price.text, details.text, image_url)
      mycursor.execute(sql, val)
      mydb.commit() 
       
      
  except:
      print(f"{link} not found")
      
  driver.close()


end_time = time.time()  

totatl_time=end_time - start_time
print(totatl_time)

dict={
      "title":product_title,
      "price":product_price,
      "details":product_details,
      "image_url":product_image_url}

with open('result.txt', 'w') as json_file:
  json.dump(dict, json_file)  









                         

