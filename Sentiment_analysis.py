#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import pos_tag
from textstat import flesch_reading_ease, syllable_count
from nltk import punkt



# In[2]:


# Loading master dictionary of positive and negative words from my download location 
positive_words = set(line.strip() for line in open(r'D:\khalid\myproject\web scraping\sentiment analysis\MasterDictionary\positive-words.txt'))
negative_words = set(line.strip() for line in open(r'D:\khalid\myproject\web scraping\sentiment analysis\MasterDictionary\negative-words.txt'))


# In[3]:


# getting stop words from  files in the stop words directory
stop_words_dir = r'D:\khalid\myproject\web scraping\sentiment analysis\StopWords'
stop_words = set()

for filename in os.listdir(stop_words_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(stop_words_dir, filename)
        with open(file_path, 'r') as file:
            stop_words.update(line.strip() for line in file)


# In[4]:


# Function to perform sentiment analysis and compute variables
def analyze_text(text):
    # Cleaning using stop words
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    
    # Creating dict of positive and negative words
    ps = len([word for word in cleaned_tokens if word in positive_words])
    ns = len([word for word in cleaned_tokens if word in negative_words])
    
    # Sentiment Analysis
    pos = (ps - ns) / ((ps + ns) + 0.000001)
    ss = (ps + ns) / (len(cleaned_tokens) + 0.000001)

    return {
        'Positive_Score': ps,
        'Negative_Score': ns,
        'Polarity_Score': pos,
        'Subjectivity_Score': ss,

    }


# In[5]:


# Loading the XLSX file into a pandas DataFrame
xlsx_file = r'D:\khalid\myproject\web scraping\wikiweb.xlsx'
df = pd.read_excel(xlsx_file)
display(df)

# Specifing the class names for article text found under inpection or URL
article_class = "mw-body-content" 
article_classb = "mw-body-content"


# In[6]:


# Function to extract title and article text under the specified class from a URL
def extract_article(url, idd):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.text if soup.title else "No title found"
        
        specified_div = soup.find('div', class_=article_class)
        specified_divb = soup.find('div', class_=article_classb)
        
        if specified_div:
            p_tags = specified_div.find_all('p')
            article_text = '\n'.join([p.get_text() for p in p_tags])
        elif specified_divb:
            p_tags = specified_divb.find_all("p")
            article_text = '\n'.join([p.get_text() for p in p_tags])
        else:
            print(f"No content found for URL: {url}")
            return
        #saving each extracted url data as text file
        filename = f"{idd}.txt"
        filepath = os.path.join(r"D:\khalid\myproject\web scraping\wikiweb_texts", filename)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(title + '\n\n')
            file.write(article_text)
            print(f"Saved article to {filename}")
                  
        # To perform sentimental analysis and compute variables passing in function
        analysis_result = analyze_text(article_text)
        
        # Saving the computed variables to the DataFrame
        for variable, value in analysis_result.items():
            df.at[index, variable] = value


# In[7]:


# Creating a directory to save text files 
os.makedirs(r"D:\khalid\myproject\web scraping\wikiweb_texts", exist_ok=True)


# In[8]:


# Iterating through the URLs and extract title and article text
for index, row in df.iterrows():
    url = row['URL']  
    idd = row['URL_ID']
    extract_article(url, idd)


# In[9]:


# Saving the updated DataFrame to a new XLSX file
output_xlsx_file = r'D:\khalid\myproject\web scraping\sentiment analysis\output_sentiment_analysis.xlsx'
df.to_excel(output_xlsx_file, index=False)
print(f"Sentimental analysis completed saved to '{output_xlsx_file}'.")


# In[ ]:





# In[ ]:




